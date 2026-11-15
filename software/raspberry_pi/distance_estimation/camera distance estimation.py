from pathlib import Path

from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time
import threading
import joblib
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = "yolo11n_ncnn_model"
DISTANCE_MODEL_PATH = ROOT_DIR / "person_distance_model.pkl"

CONFIDENCE = 0.3
IMAGE_SIZE = 320
CAMERA_SIZE = (640, 480)

MIN_DISTANCE = 1.0
MAX_DISTANCE = 2.5

print("Loading YOLO11n NCNN...")
model = YOLO(MODEL_PATH)

print("Loading distance estimation model...")
distance_data = joblib.load(DISTANCE_MODEL_PATH)
distance_model = distance_data["model"]
features = distance_data["features"]

supported_features = {"height", "area"}
if not features or not set(features).issubset(supported_features):
    raise ValueError(f"Unsupported distance-model features: {features}")

print("Distance model:", distance_data["model_name"])
print("Features:", features)

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": CAMERA_SIZE, "format": "RGB888"},
    buffer_count=4,
    queue=False,
)
picam2.configure(config)
picam2.start()
time.sleep(2)

latest_frame = None
frame_lock = threading.Lock()
running = True
capture_ms = 0.0


def capture_frames():
    global latest_frame, capture_ms

    while running:
        start = time.perf_counter()
        frame = picam2.capture_array()
        elapsed = (time.perf_counter() - start) * 1000

        with frame_lock:
            latest_frame = frame
            capture_ms = elapsed


camera_thread = threading.Thread(target=capture_frames, daemon=True)
camera_thread.start()

print("YOLO11n + Distance Estimation Started")
print("Press q to quit.")

fps = 0.0
frame_count = 0
fps_start = time.perf_counter()

try:
    while True:
        with frame_lock:
            frame = latest_frame
            current_capture_ms = capture_ms

        if frame is None:
            time.sleep(0.001)
            continue

        inference_start = time.perf_counter()
        results = model.predict(
            source=frame,
            imgsz=IMAGE_SIZE,
            conf=CONFIDENCE,
            classes=[0],
            verbose=False,
        )
        inference_ms = (time.perf_counter() - inference_start) * 1000

        draw_start = time.perf_counter()
        annotated = results[0].plot()

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            height = float(y2 - y1)
            width = float(x2 - x1)
            area = height * width

            values = {"height": height, "area": area}
            input_data = pd.DataFrame(
                [[values[feature] for feature in features]],
                columns=features,
            )

            predicted_distance = float(distance_model.predict(input_data)[0])

            if MIN_DISTANCE <= predicted_distance <= MAX_DISTANCE:
                label = f"Distance: {predicted_distance:.2f} m"
                color = (0, 255, 0)
            else:
                label = f"Out of range: {predicted_distance:.2f} m"
                color = (0, 165, 255)

            cv2.putText(
                annotated,
                label,
                (int(x1), max(25, int(y1) - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

        draw_ms = (time.perf_counter() - draw_start) * 1000

        frame_count += 1
        elapsed = time.perf_counter() - fps_start

        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            fps_start = time.perf_counter()

        metrics = [
            f"YOLO11n | FPS: {fps:.1f}",
            f"Confidence: {CONFIDENCE}",
            f"Capture: {current_capture_ms:.1f} ms",
            f"Inference: {inference_ms:.1f} ms",
            f"Drawing: {draw_ms:.1f} ms",
        ]

        for index, metric in enumerate(metrics):
            cv2.putText(
                annotated,
                metric,
                (10, 25 + index * 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow("YOLO11n + Distance Estimation", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    pass

finally:
    running = False
    camera_thread.join(timeout=2)
    picam2.stop()
    cv2.destroyAllWindows()
    print("Detection stopped.")
