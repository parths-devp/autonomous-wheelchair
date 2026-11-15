# Ultrasonic sensors

The Raspberry Pi reads three HC-SR04 sensors using gpiozero and sequential measurements.

| Sensor | Trigger (BCM) | Echo (BCM) | JSON field |
|---|---:|---:|---|
| Front | 17 | 27 | \`front_cm\` |
| Right | 22 | 5 | \`right_cm\` |
| Left | 23 | 24 | \`left_cm\` |

The script averages up to 10 valid readings per sensor and writes the latest values with a timestamp to \`/dev/shm/ultrasonic_distances.json\`.

A reading of \`-1.0\` means no valid echo was received during the measurement attempts. The JSON field names and timestamp format are retained for the Raspberry Pi obstacle-monitoring application.

Run this script with the system Python environment where gpiozero is installed. Do not connect an HC-SR04 5 V ECHO output directly to a Raspberry Pi GPIO pin. Use a suitable voltage divider or level shifter.
