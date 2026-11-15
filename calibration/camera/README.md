# Camera calibration

The calibration script is `camera_calibration.py`. It uses Picamera2, OpenCV, and a printed checkerboard.

## Recorded camera setup

- Camera: Raspberry Pi Camera Module Rev 1.3, OV5647
- Calibration image size: 1296 × 972 pixels
- Checkerboard internal corners: 11 × 7
- Checker square size: 0.02 m
- Requested captures: 20
- Recorded RMS reprojection error: approximately 0.36 pixels

Previously recorded intrinsic matrix:

```text
[[1412.1090,    0.0000, 651.1135],
 [   0.0000, 1422.9038, 478.6244],
 [   0.0000,    0.0000,   1.0000]]
```

Previously recorded distortion coefficients:

```text
[0.214035, -0.809550, 0.001876, 0.001345, 0.952222]
```

These values correspond to the 1296 × 972 calibration resolution. Recalibrate if the camera module, lens, focus, or image resolution changes.

## Run

Use the Raspberry Pi system environment where Picamera2 and OpenCV are available:

```bash
python3 calibration/camera/camera_calibration.py
```

Show the checkerboard at different positions, tilts, and distances. Press SPACE only when the pattern is detected; press Q to finish. The script saves captured images in `calibration_images/` and writes `camera_calibration.npz` in the current working directory.

The generated NPZ file and calibration images are not committed. The current YOLO distance-estimation script does not automatically load these calibration parameters.