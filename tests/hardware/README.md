# Hardware tests

Record each test date, hardware revision, setup, measured result, and pass/fail decision.

## HC-SR04 sensors

- Confirm each trigger and echo pin against the wiring table.
- Verify the ECHO voltage divider or level shifter before connecting the Pi.
- Compare readings with a tape-measured target distance.
- Record repeated measurements separately for front, left, and right.
- Test angled and soft targets and note missed echoes.

## Camera

- Confirm the OV5647 is detected by \`rpicam-hello --list-cameras\`.
- Check the capture resolution and camera orientation.
- Verify the checkerboard calibration at the resolution used by the calibration script.

## Arduino and TB6600

- Check the 12 V driver supply and motor wiring against the driver's terminal labels.
- Verify D2 STEP, D3 DIR, and ground wiring.
- Confirm driver current and microstep settings.
- Test F, B, and S with the wheels raised.
- Measure stop response and verify the physical emergency stop.

Do not mark a test as passed without recording its measured result. No complete hardware validation report is currently committed.