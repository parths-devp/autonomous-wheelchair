
from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time
import threading

MODEL_PATH = "yolo11n_ncnn_model"
CONFIDENCE = 0.3
IMAGE_SIZE = 320
CAMERA_SIZE = (640, 480)


model = YOLO(MODEL_PATH)


picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={
        "size": CAMERA_SIZE,
        "format": "RGB888"
    },
    buffer_count=4
)

picam2.configure(config)
picam2.start()


frame = None
lock = threading.Lock()
running = True


def capture_frames():
    global frame, running

    while running:
        new_frame = picam2.capture_array()

        with lock:
            frame = new_frame


camera_thread = threading.Thread(
    target=capture_frames,
    daemon=True
)

camera_thread.start()

print("YOLO11n Person Detection Started")
print("Press Q to quit")

try:
    while True:
        with lock:
            if frame is None:
                continue

            current_frame = frame.copy()

        start_time = time.time()

        
        results = model.predict(
            current_frame,
            imgsz=IMAGE_SIZE,
            conf=CONFIDENCE,
            classes=[0],
            verbose=False
        )

        
        annotated_frame = results[0].plot()

        
        inference_time = time.time() - start_time
        fps = 1.0 / inference_time if inference_time > 0 else 0

        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "YOLO11n - Person Detection",
            annotated_frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    running = False
    camera_thread.join(timeout=1)

    picam2.stop()
    cv2.destroyAllWindows()
