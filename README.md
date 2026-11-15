# Autonomous Wheelchair

An experimental assistive wheelchair prototype intended to help a visually impaired user detect nearby obstacles and make basic movement decisions.

## Project status

The repository contains working subsystem code for YOLO11n person detection, camera-based person-distance estimation, three HC-SR04 sensors, and prototype serial motor-control software. The Arduino motor firmware and Raspberry Pi obstacle controller have been added as integration-stage code and still require hardware verification together. The complete wheelchair is not an autonomous or safety-certified mobility device.

## System overview

| Subsystem | Current implementation |
|---|---|
| Main computer | Raspberry Pi 4 Model B |
| Camera | OV5647 Raspberry Pi Camera Module |
| Object detection | YOLO11n NCNN, COCO person class only |
| Camera distance estimate | Linear regression using person bounding-box height and/or area |
| Proximity sensing | Three HC-SR04 sensors: left, front/centre, right |
| Sensor interface | Raspberry Pi GPIO using gpiozero |
| Motor command interface | Raspberry Pi USB serial to Arduino Uno |
| Motor driver | TB6600 |
| Drive motor | NEMA 23 stepper motor |
| Steering prototype | Separate NEMA 17 gear-driven steering mechanism |

## Data flow

\`\`\`text
OV5647 camera -> YOLO11n person detection -> bounding-box features
                                             |
                                             v
                                    person distance model

HC-SR04 left / front / right -> JSON sensor readings
                                             |
                                             v
                                  obstacle motor controller
                                             |
                                    USB serial F / S
                                             |
                                             v
Arduino Uno -> TB6600 -> NEMA 23 drive motor
\`\`\`

The camera distance model and ultrasonic sensors provide different measurements. A single ultrasonic reading is not automatically the depth of every object detected by the camera. Object association requires sensor direction, field of view, mounting geometry, and additional validation.

## Repository structure

- \`calibration/\` — camera and ultrasonic calibration procedures.
- \`docs/\` — project overview, architecture, setup, hardware, and wiring guidance.
- \`hardware/\` — component list, CAD organization, electronics, and calibration records.
- \`machine_learning/\` — person-distance dataset and model training.
- \`media/\` — project photographs and demonstration videos.
- \`software/arduino/\` — Arduino motor-controller firmware.
- \`software/raspberry_pi/\` — object detection, distance estimation, ultrasonic sensing, and motor control.
- \`tests/\` — subsystem and integration test procedures.

## Quick start

The camera/YOLO application and the ultrasonic GPIO application use separate Python environments. Keep that separation unless it has been deliberately tested.

Train the distance model from the repository root:

\`\`\`bash
python3 machine_learning/training/training.py
\`\`\`

This creates \`person_distance_model.pkl\` in the repository root. The inference script also requires the YOLO11n NCNN model directory \`yolo11n_ncnn_model\`, which is not committed.

Run the three-sensor application using system Python on the Raspberry Pi:

\`\`\`bash
python3 software/raspberry_pi/ultrasonic_sensors/ultrasonic.py
\`\`\`

Upload \`software/arduino/motor_controller/motor_controller.ino\` to the Arduino Uno. For a raised-wheel serial test, run:

\`\`\`bash
python3 software/raspberry_pi/motor_control/motor_test.py
\`\`\`

The automatic obstacle controller is:

\`\`\`bash
python3 software/raspberry_pi/motor_control/obstacle_motor_controller.py
\`\`\`

Do not run the automatic controller until the motor direction, emergency stop, sensor readings, serial connection, and stop behaviour have been checked with the drive wheels raised.

## Safety

This is a research prototype, not a certified mobility aid. It must not be used as the sole means of mobility or relied upon to prevent collisions. Use a physical emergency stop, keep the wheels raised during initial motor tests, and perform supervised low-speed tests in a controlled area. Invalid or stale front-sensor data is treated as a stop condition by the obstacle controller.

## Performance and validation

Previously recorded camera calibration RMS reprojection error is approximately 0.36 pixels. The person-distance dataset contains 120 samples across 1.0 m, 1.5 m, 2.0 m, and 2.5 m. These dataset measurements do not establish generalization to new people, camera positions, lighting, or environments. Record measured test conditions and results before making accuracy or safety claims.

## License

No open-source license has been selected. Until a license is added, the repository remains subject to the default copyright rules.