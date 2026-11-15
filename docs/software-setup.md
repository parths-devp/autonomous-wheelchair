# Software Setup

## Raspberry Pi platform

The current development system is a Raspberry Pi 4 Model B Rev 1.5 running Debian GNU/Linux 13 (Trixie), aarch64, with Python 3.13.5. The camera is an OV5647 module and is accessed through Picamera2.

## Camera and YOLO environment

The camera and YOLO application runs in a dedicated virtual environment with system site packages enabled so that Picamera2 is available. The working environment path used during development was:

```bash
source ~/yolov8_pi/venv/bin/activate
```

Check camera detection:

```bash
rpicam-hello --list-cameras
python3 -c "from picamera2 import Picamera2; print('Picamera2 OK')"
```

The object-detection scripts require Picamera2, Ultralytics with NCNN support, and OpenCV. The NCNN model directory `yolo11n_ncnn_model` is generated/exported separately and is not committed to this repository.

Run person detection:

```bash
python3 software/raspberry_pi/object_detection/object_detection_person.py
```

Run person-distance inference after training the regression model:

```bash
python3 "software/raspberry_pi/distance_estimation/camera distance estimation.py"
```

## Machine-learning training environment

The training script uses Python packages `numpy`, `pandas`, `scikit-learn`, and `joblib`. Run it from the repository root:

```bash
python3 machine_learning/training/training.py
```

It creates `person_distance_model.pkl` in the repository root. The generated model file is not committed.

## Ultrasonic GPIO environment

Run the HC-SR04 script using Raspberry Pi system Python where gpiozero is installed:

```bash
python3 software/raspberry_pi/ultrasonic_sensors/ultrasonic.py
```

Keep this separate from the YOLO virtual environment. The script writes `/dev/shm/ultrasonic_distances.json`.

## Motor-control environment

Install pyserial in the Python environment used for motor control:

```bash
python3 -m pip install pyserial
```

Upload `software/arduino/motor_controller/motor_controller.ino` to an Arduino Uno. The Pi scripts use USB serial, normally `/dev/ttyACM0`, at 115200 baud:

```bash
python3 software/raspberry_pi/motor_control/motor_test.py
python3 software/raspberry_pi/motor_control/obstacle_motor_controller.py
```

Test the manual commands with the wheels raised before running the automatic controller.

## Environment separation

- Picamera2 and camera capture: Raspberry Pi system packages exposed to the camera/YOLO virtual environment.
- YOLO and NCNN inference: dedicated virtual environment.
- HC-SR04 GPIO: system Python with gpiozero.
- Motor serial control: Python environment with pyserial.
- Arduino firmware: Arduino IDE, Arduino Uno board support.

Record package versions when reproducing experiments. Do not assume that a virtual environment on a different Pi has the same packages.