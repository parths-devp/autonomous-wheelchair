# Autonomous Wheelchair

An assistive wheelchair prototype designed to help visually impaired users detect nearby obstacles and navigate more safely using computer vision and distance sensors.

## Project overview

The prototype combines a Raspberry Pi camera, YOLO-based object detection, distance estimation, three ultrasonic sensors, and a motor-control system. Development is ongoing; features and performance will be documented as they are tested.

## Current system

- **Vision:** Raspberry Pi Camera with YOLO object detection (YOLO11n, NCNN).
- **Distance estimation:** A trained model estimates the distance to detected people from bounding-box measurements.
- **Proximity sensing:** Three HC-SR04 ultrasonic sensors monitor the left, centre, and right directions.
- **Motion control:** Raspberry Pi, Arduino Uno, TB6600 stepper driver, and NEMA 23 stepper motor.
- **Planned behaviour:** Forward and backward movement, obstacle stop, and automatic forward resume after the path clears.

## Architecture

```text
Raspberry Pi Camera
        |
        v
YOLO object detection
        |
        v
Bounding-box measurements
        |
        v
Object distance estimation ----+
                               |
HC-SR04 (left / centre / right)|
        |                      |
        +----> Obstacle logic <-+
                    |
                    v
              Motion command
                    |
                    v
          Arduino Uno -> TB6600
                    |
                    v
               Stepper motor
```

## Repository layout

- `docs/` — project, architecture, hardware, and software documentation.
- `hardware/` — CAD, electronics, wiring, and calibration resources.
- `software/raspberry_pi/` — camera, detection, distance, sensors, and integration code.
- `software/arduino/` — Arduino-side firmware.
- `machine_learning/` — training, evaluation, datasets, and model notes.
- `calibration/` — camera and sensor calibration files.
- `tests/` — hardware, software, and integration tests.
- `media/` — project photographs and demonstration videos.

## Safety note

This is an experimental prototype, not a certified mobility aid. Do not use it as the sole means of mobility or rely on it to protect a person from collisions. Test with the wheels raised or the drive system otherwise made safe, then conduct supervised low-speed tests in a controlled area.

## Development status

The repository structure and initial documentation are being established. Implementation details, test results, wiring diagrams, CAD files, and trained model artefacts will be added as they are verified.

## License

No open-source license has been selected yet. Unless a license is added, the repository's contents remain subject to the default copyright rules.
