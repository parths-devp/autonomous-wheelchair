# Project Overview

## Goal

Develop an autonomous assistive wheelchair prototype that can identify obstacles in its surroundings and make basic movement decisions to improve mobility for visually impaired users.

## Core subsystems

1. **Camera perception:** Capture frames using the Raspberry Pi Camera.
2. **Object detection:** Run a lightweight YOLO model to identify objects and return bounding boxes.
3. **Distance estimation:** Estimate the distance to supported detected objects using calibrated image measurements and a trained regression model.
4. **Proximity sensing:** Use three HC-SR04 sensors positioned left, centre, and right for direct range measurements.
5. **Obstacle logic:** Combine perception and proximity information to decide when motion should stop or resume.
6. **Drive control:** Send motion commands from the Raspberry Pi to an Arduino Uno controlling a TB6600 driver and NEMA 23 stepper motor.

## Current scope

The initial drive behaviour is intentionally limited to forward, backward, and stop. The intended safety behaviour is to stop when an obstacle is detected and resume forward movement only after the obstacle clears.

## Development principles

- Keep perception, sensing, decision logic, and motor control as separate modules.
- Record sensor geometry, calibration settings, and test conditions.
- Validate each subsystem independently before integration.
- Treat all performance figures as measured results, not assumptions.
- Keep the prototype supervised during testing.
