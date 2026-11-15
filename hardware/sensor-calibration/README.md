# Sensor calibration

Use this directory for measured calibration records for the camera and the three HC-SR04 sensors.

## Records to maintain

For each sensor, record:

- Sensor identifier and physical mounting position.
- GPIO trigger and echo pins.
- Reference distance measured with a tape.
- Raw repeated readings in centimetres.
- Mean reading, absolute error, and maximum error.
- Target material, target angle, and environmental conditions.
- Date, supply voltage, and any correction factor.

The current HC-SR04 implementation averages up to 10 valid readings and writes the latest values to `/dev/shm/ultrasonic_distances.json`. No complete sensor calibration dataset or verified correction coefficients have been committed yet.

Keep raw measurements as well as calculated results so that correction methods can be reviewed later.