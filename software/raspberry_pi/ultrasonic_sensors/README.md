# Ultrasonic sensors

The Raspberry Pi reads three HC-SR04 sensors sequentially using gpiozero and system Python.

## GPIO mapping

BCM numbering is used.

| Sensor | Trigger | Echo | JSON field |
|---|---:|---:|---|
| Front/centre | GPIO 17 | GPIO 27 | `front_cm` |
| Right | GPIO 22 | GPIO 5 | `right_cm` |
| Left | GPIO 23 | GPIO 24 | `left_cm` |

## Operation

Script: `ultrasonic.py`

The script takes up to 10 readings per sensor, averages valid echoes, and writes a JSON record to:

```text
/dev/shm/ultrasonic_distances.json
```

Example structure:

```json
{
  "front_cm": 73.0,
  "right_cm": 21.1,
  "left_cm": 31.4,
  "timestamp": 1794686682.74
}
```

Distances are in centimetres and the timestamp is Unix time. A value of `-1.0` means that no valid echo was received during that sensor's measurement attempts. The file is replaced atomically so that a reader does not normally see a partially written JSON record.

Run with the Raspberry Pi system Python where gpiozero is installed:

```bash
python3 software/raspberry_pi/ultrasonic_sensors/ultrasonic.py
```

Keep this process in the system Python environment. The YOLO/Picamera2 application runs in a separate virtual environment.

## Electrical warning

HC-SR04 ECHO can output 5 V. Raspberry Pi GPIO inputs are 3.3 V only. Use a correctly sized voltage divider or level shifter on every ECHO line. Do not connect a 5 V ECHO signal directly to a Raspberry Pi.

The sensor readings are proximity measurements in three directions. They are not automatically associated with individual YOLO bounding boxes.