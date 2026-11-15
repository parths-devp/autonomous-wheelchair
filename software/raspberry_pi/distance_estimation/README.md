# Distance estimation

The current distance-estimation pipeline predicts the distance to a detected person from YOLO bounding-box measurements. It is a separate estimate from the HC-SR04 readings.

## Dataset and training

Dataset: `machine_learning/datasets/person_distance_training.csv`

The dataset has 120 samples at 1.0 m, 1.5 m, 2.0 m, and 2.5 m. The training script compares linear regression models using bounding-box height, area, and both features.

From the repository root, run:

```bash
python3 machine_learning/training/training.py
```

The script writes `person_distance_model.pkl` to the repository root. Keep the training and inference feature names consistent: `height` and/or `area`.

## Camera inference

Script: `camera distance estimation.py`

Requirements include Picamera2, OpenCV, Ultralytics, joblib, and pandas, plus the external `yolo11n_ncnn_model` directory. Run it in the camera/YOLO virtual environment:

```bash
python3 "software/raspberry_pi/distance_estimation/camera distance estimation.py"
```

The current script detects COCO class 0 (person), uses 640 × 480 camera frames and YOLO image size 320, and displays predictions within the configured 1.0–2.5 m range.

## Limitations

The current model is trained from a small dataset with four reference distances. A random stratified test split does not demonstrate reliable interpolation or generalization to new people, lighting, camera poses, or scenes. Validate with independent distances and subjects before using predictions for obstacle safety.

The current inference script does not apply the saved camera intrinsic matrix or distortion correction. The camera calibration is documented separately.