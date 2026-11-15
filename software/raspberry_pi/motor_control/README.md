# Raspberry Pi motor control

This directory contains the Pi-side serial utilities for the Arduino Uno and TB6600 drive motor.

## Files

- \`motor_test.py\` — interactive serial test utility.
- \`obstacle_motor_controller.py\` — reads front HC-SR04 JSON data and sends automatic forward/stop commands.

## Serial connection

The current setup uses a USB connection, typically \`/dev/ttyACM0\`, at 115200 baud. The Arduino sketch uses:

| Command | Action |
|---|---|
| \`F\` | Forward |
| \`B\` | Backward |
| \`S\` | Stop |

Install pyserial in the Python environment used for motor control:

\`\`\`bash
python3 -m pip install pyserial
\`\`\`

Run the manual test with the drive wheels raised:

\`\`\`bash
python3 software/raspberry_pi/motor_control/motor_test.py
\`\`\`

## Obstacle behaviour

The automatic controller reads \`/dev/shm/ultrasonic_distances.json\`, specifically \`front_cm\` and \`timestamp\`.

- At or below 15 cm: send STOP.
- At or above 25 cm: send FORWARD.
- Between 15 cm and 25 cm: retain the previous command (hysteresis).
- Missing, invalid, or stale front data: send STOP.

The 5-second sensor timeout accommodates the sequential averaging cycle; confirm it against the actual sensor update rate. The automatic controller only uses the front sensor for its current stop/resume decision.

## Safety and status

This is prototype integration code, not a certified collision-avoidance system. Verify command direction, stop latency, sensor freshness, motor power isolation, and physical emergency stop before enabling wheel motion. Start tests with wheels raised and use supervised low-speed tests only.