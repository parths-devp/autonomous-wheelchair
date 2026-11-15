# Datasets

## Person distance training data

File: `person_distance_training.csv`

The committed dataset contains 120 samples: 30 samples at each measured distance of 1.0 m, 1.5 m, 2.0 m, and 2.5 m.

| Column | Meaning |
|---|---|
| `Distance (m)` | Reference distance to the person, in metres |
| `Sample` | Sample number within the distance group |
| `Height (px)` | Detected person bounding-box height |
| `Area (px^2)` | Detected person bounding-box area |

The training script maps these columns to the feature names `distance`, `height`, and `area`. It compares linear regression using height, area, and both features, then saves the best model by held-out mean absolute error.

## Limitations

The data covers four discrete reference distances and a limited capture setup. A random stratified split evaluates held-out samples from the same four distance groups; it does not prove accuracy at unseen distances, with different people, camera angles, lighting, or environments. Collect independent test data before reporting general distance-estimation accuracy.

Do not add personally identifying images or private recordings. Keep dataset units and collection conditions documented.