# System Architecture

## Data flow

1. Picamera2 captures camera frames on the Raspberry Pi.
2. YOLO inference detects supported object classes and produces bounding boxes.
3. Bounding-box features are passed to the distance-estimation module where applicable.
4. Three HC-SR04 sensors provide left, centre, and right proximity readings.
5. Obstacle logic evaluates the available readings and generates a motion state.
6. The Raspberry Pi communicates the motion command to the Arduino Uno.
7. The Arduino drives the TB6600 stepper driver.

## Software/environment separation

The camera and YOLO application runs in its dedicated Python virtual environment with Picamera2 available through system site packages where required. The ultrasonic GPIO application uses the Raspberry Pi system Python and gpiozero. Preserve this separation unless the integration is deliberately redesigned and tested.

## Important integration constraint

A single ultrasonic reading does not automatically provide the depth of every object detected in a camera frame. Sensor direction, field of view, mounting geometry, and object association must be considered before assigning a range measurement to a particular bounding box.

## Planned control states

- `STOP`: default safe state or obstacle detected.
- `FORWARD`: move forward when the path is clear.
- `BACKWARD`: move backward when explicitly commanded and safe.

The exact thresholds, timing, communication protocol, and fail-safe behaviour must be documented alongside the implementation after testing.
