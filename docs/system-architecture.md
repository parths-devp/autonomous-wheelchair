# System Architecture

## Perception and sensing

1. Picamera2 captures 640 × 480 frames from the OV5647 camera.
2. YOLO11n NCNN detects COCO person class objects and returns bounding boxes.
3. Bounding-box height and area can be passed to the trained person-distance regression model.
4. Three HC-SR04 sensors independently measure front/centre, left, and right proximity.
5. The ultrasonic process writes the latest readings and Unix timestamp to `/dev/shm/ultrasonic_distances.json`.

Camera distance estimates and ultrasonic readings are separate sources. One ultrasonic return cannot be assigned as the depth of every detected camera object without a sensor-to-object association method.

## Motion-control path

1. `obstacle_motor_controller.py` reads the front sensor distance and timestamp.
2. At or below 15 cm it sends STOP.
3. At or above 25 cm it sends FORWARD.
4. Between 15 cm and 25 cm it retains the previous motion state.
5. Missing, invalid, or stale front data causes STOP.
6. The Pi sends single-character commands over USB serial at 115200 baud.
7. The Arduino Uno generates STEP and DIR signals for the TB6600 driver.

The Arduino command set is `F` (forward), `B` (backward), and `S` (stop). While motion is active, the Pi sends an `H` heartbeat. The Arduino stops the motor if no heartbeat is received for 750 ms.

## Software/environment separation

- Camera and YOLO: dedicated virtual environment with system site packages enabled for Picamera2.
- Ultrasonic GPIO: system Python with gpiozero.
- Motor serial controller: Python with pyserial.
- Motor pulse generation: Arduino Uno firmware.

## Current limitations

The automatic controller currently uses only the front sensor and does not steer using left/right measurements. YOLO currently detects people only. Distance regression is trained on a limited four-distance dataset. Camera calibration values are documented separately but are not applied by the current distance-inference script.

All thresholds and timing values are prototype settings. Validate them on the actual hardware before any supervised low-speed movement.