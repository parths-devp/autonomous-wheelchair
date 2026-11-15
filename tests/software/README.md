# Software tests

Use repeatable test data and record software versions with each result.

## Distance-model training

- Confirm the CSV path resolves from the training script.
- Confirm the expected columns are present.
- Check the reported dataset shape and distance distribution.
- Record MAE, RMSE, and R² for each feature set.
- Confirm `person_distance_model.pkl` is created and can be loaded.

## Object detection

- Confirm the NCNN model directory is available.
- Check that only COCO person class detections are returned.
- Record FPS, inference time, confidence threshold, and camera resolution.

## Ultrasonic JSON interface

- Confirm the file contains `front_cm`, `right_cm`, `left_cm`, and `timestamp`.
- Confirm distances are in centimetres.
- Confirm invalid measurements are represented by -1.0.
- Confirm the file is replaced without partial JSON reads.

## Motor-control software

- Test F, B, and S serial commands with the wheels raised.
- Test missing, malformed, invalid, and stale sensor data.
- Confirm the obstacle controller stops on invalid data and applies 15 cm / 25 cm hysteresis.

The repository does not yet contain an automated test suite for the hardware interfaces. Manual results should be stored with dates and test conditions.