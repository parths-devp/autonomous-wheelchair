# Software Setup

## Raspberry Pi

The project uses Raspberry Pi OS on a Raspberry Pi 4.

### Camera and object detection environment

The Picamera2 and YOLO application is maintained in a dedicated virtual environment. Picamera2 may be provided by system Python, so the environment was configured to include system site packages.

Typical checks:

```bash
rpicam-hello --list-cameras
python -c "from picamera2 import Picamera2; print('Picamera2 OK')"
```

Activate the project's actual virtual environment before running camera and YOLO scripts. Install dependencies from a pinned requirements file once that file is added to the repository.

### Ultrasonic GPIO environment

The HC-SR04 sensor application currently uses system Python with gpiozero. Keep it separate from the YOLO virtual environment unless dependency compatibility is verified.

### Arduino

Arduino firmware is stored under `software/arduino/`. Open the relevant sketch in Arduino IDE, select Arduino Uno, verify the pin assignments, and upload only after checking the motor driver wiring.

## Reproducibility

When adding code, include:
- Python version and operating-system version.
- Dependency versions or a requirements file.
- Model name and input image size.
- GPIO pin numbering convention.
- Sensor mounting positions and calibration constants.
- Arduino pin mapping and serial protocol, if used.
