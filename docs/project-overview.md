# Project Overview

## Goal

Develop an experimental assistive wheelchair prototype that can detect nearby obstacles and make basic movement decisions to support mobility for a visually impaired user.

## Subsystems

1. **Camera capture:** OV5647 camera frames are captured through Picamera2 on the Raspberry Pi 4.
2. **Object detection:** YOLO11n NCNN currently detects the COCO person class and returns bounding boxes.
3. **Person distance estimation:** A linear regression model estimates person distance from bounding-box height and/or area. Training data currently covers four reference distances from 1.0 m to 2.5 m.
4. **Proximity sensing:** Three HC-SR04 sensors measure front/centre, left, and right distances.
5. **Obstacle control:** The Raspberry Pi motor controller currently uses the front sensor with a 15 cm stop threshold and 25 cm clear threshold. Invalid or stale sensor data causes STOP.
6. **Drive control:** USB serial commands are sent to an Arduino Uno, which generates STEP and DIR signals for a TB6600 and NEMA 23 drive motor.

## Current code

- `software/raspberry_pi/object_detection/object_detection_person.py` — person-only YOLO detection.
- `machine_learning/training/training.py` — trains and evaluates the person-distance regression models.
- `software/raspberry_pi/distance_estimation/camera distance estimation.py` — camera inference and person-distance display.
- `software/raspberry_pi/ultrasonic_sensors/ultrasonic.py` — three-sensor JSON producer.
- `software/raspberry_pi/motor_control/obstacle_motor_controller.py` — front-sensor obstacle stop and forward resume.
- `software/raspberry_pi/motor_control/motor_test.py` — manual serial motor test.
- `software/arduino/motor_controller/motor_controller.ino` — Arduino TB6600 pulse controller.

## Current scope and limitations

The motor interface supports forward, backward, and stop commands. The automatic obstacle controller currently makes forward/stop decisions from the front HC-SR04 only; left and right measurements are logged but not yet used for steering. Camera detections are person-only. The camera-based regression output is not fused with individual ultrasonic returns because a single ultrasonic measurement cannot provide depth for every object in the camera frame.

## Development principles

- Keep camera inference and GPIO sensing in their separate Python environments.
- Validate each subsystem independently before integration.
- Record calibration data and test conditions.
- Report measured performance only; do not treat model evaluation on the current dataset as generalization evidence.
- Keep a physical emergency stop and supervised operation throughout development.