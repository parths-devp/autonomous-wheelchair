
from picamera2 import Picamera2
import cv2
import numpy as np
import time
import os


CHECKERBOARD = (11, 7)
SQUARE_SIZE = 0.02
IMAGE_SIZE = (1296, 972)
REQUIRED_IMAGES = 20

SAVE_DIR = "calibration_images"
os.makedirs(SAVE_DIR, exist_ok=True)


objp = np.zeros(
    (CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    np.float32
)

objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE

objpoints = []
imgpoints = []


picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": IMAGE_SIZE, "format": "RGB888"}
)

picam2.configure(config)
picam2.start()
time.sleep(2)

count = 0
last_capture = 0

print("Camera calibration started.")
print("Show checkerboard and press SPACE to capture.")
print("Press Q to finish.")

try:
    while count < REQUIRED_IMAGES:

        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        ret, corners = cv2.findChessboardCorners(
            gray,
            CHECKERBOARD,
            None
        )

        display = frame.copy()

        if ret:
            corners_refined = cv2.cornerSubPix(
                gray,
                corners,
                (11, 11),
                (-1, -1),
                (
                    cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER,
                    30,
                    0.001
                )
            )

            cv2.drawChessboardCorners(
                display,
                CHECKERBOARD,
                corners_refined,
                ret
            )

            cv2.putText(
                display,
                "Checkerboard detected - Press SPACE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        else:
            cv2.putText(
                display,
                "Checkerboard not detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        cv2.putText(
            display,
            f"Images: {count}/{REQUIRED_IMAGES}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.imshow("Camera Calibration", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' ') and ret:
            if time.time() - last_capture > 1:

                objpoints.append(objp.copy())
                imgpoints.append(corners_refined.copy())

                count += 1
                last_capture = time.time()

                cv2.imwrite(
                    f"{SAVE_DIR}/image_{count:02d}.jpg",
                    cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                )

                print(f"Captured image {count}/{REQUIRED_IMAGES}")

        elif key == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()

if count < 10:
    print("Not enough images for reliable calibration.")
    exit()


print("Calculating camera parameters...")

ret, camera_matrix, dist_coeffs, rvecs, tvecs = (
    cv2.calibrateCamera(
        objpoints,
        imgpoints,
        IMAGE_SIZE,
        None,
        None
    )
)

print("\nCalibration Results")
print("-------------------")

print("RMS Error:", ret)
print("\nCamera Matrix:\n", camera_matrix)
print("\nDistortion Coefficients:\n", dist_coeffs)


np.savez(
    "camera_calibration.npz",
    camera_matrix=camera_matrix,
    dist_coeffs=dist_coeffs,
    image_size=IMAGE_SIZE,
    rms_error=ret
)

print("\nSaved: camera_calibration.npz")
