# Object detection

The current Raspberry Pi object-detection script is `object_detection_person.py`.

## Configuration

- Model: YOLO11n exported to NCNN format
- Model directory: `yolo11n_ncnn_model` (external model artifact; not committed)
- Camera: OV5647 through Picamera2
- Camera frame size: 640 × 480
- YOLO inference image size: 320
- Confidence threshold: 0.3
- Class filter: COCO class 0 (person)

The script captures frames in a background thread, performs YOLO inference, draws detections, and displays an FPS estimate. Press Q to exit.

## Run

Activate the Raspberry Pi camera/YOLO virtual environment and run:

```bash
python3 software/raspberry_pi/object_detection/object_detection_person.py
```

The environment must provide Picamera2, Ultralytics with NCNN support, and OpenCV. Picamera2 is supplied through the Raspberry Pi system packages in the current setup, so the virtual environment may need system site packages enabled.

This script is person-only. It does not currently detect all planned classes such as chairs, tables, stairs, doors, poles, or vehicles. It also does not perform depth estimation or obstacle-to-motor control.