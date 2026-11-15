# Integration tests

Integrate one subsystem at a time. Keep the wheelchair mechanically supported and the drive wheels raised until the motor and stop logic have been verified.

## Staged test sequence

1. Run YOLO person detection independently and confirm stable camera frames.
2. Train the person-distance model and verify that inference loads the generated model.
3. Run the ultrasonic process and confirm that all three JSON fields and the timestamp update.
4. Test Arduino F, B, and S commands using `motor_test.py`.
5. Run the obstacle controller with the motor disabled or wheels raised.
6. Simulate safe, near-obstacle, invalid, missing, and stale front-sensor data.
7. Verify stop at or below 15 cm, resume at or above 25 cm, and state retention between thresholds.
8. Only after these tests pass, conduct supervised low-speed tests in a controlled area.

## Required failure tests

- Ultrasonic JSON file missing.
- JSON malformed or missing required fields.
- Front distance is -1 or zero.
- Sensor timestamp is stale.
- Serial device disconnects.
- Arduino resets or loses power.
- Obstacle appears while moving forward.
- Obstacle clears after a stop.

Record the stop response time, sensor update interval, serial status, and test conditions. The integrated controller is experimental and must not be treated as a certified safety system.