# Ultrasonic calibration

The prototype uses three HC-SR04 sensors mounted to measure the front/centre, left, and right directions.

## Sensor positions and GPIO

| Direction | Trigger (BCM) | Echo (BCM) |
|---|---:|---:|
| Front/centre | 17 | 27 |
| Right | 22 | 5 |
| Left | 23 | 24 |

## Calibration procedure

1. Mount each sensor in its final position and keep its face perpendicular to the target surface.
2. Measure known target distances with a tape measure.
3. Record repeated readings at several distances across the intended operating range.
4. Calculate mean absolute error and maximum absolute error for each sensor separately.
5. Repeat with representative target materials and orientations.
6. Record sensor-to-wheelchair reference offsets and any correction factors in a dated results table.

The current sensor script averages up to 10 valid echoes per sensor. No verified per-sensor correction coefficients or complete calibration dataset are currently stored in this directory. Do not assume that all three sensors have identical errors.

## Electrical safety

HC-SR04 ECHO is a 5 V signal. Use a voltage divider or level shifter on each ECHO line before connecting it to a Raspberry Pi GPIO input. Never connect a 5 V ECHO output directly to a Pi GPIO pin.