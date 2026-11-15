# Arduino sensor interface

The current HC-SR04 sensors are connected directly to the Raspberry Pi and read by `software/raspberry_pi/ultrasonic_sensors/ultrasonic.py` using gpiozero. No Arduino-side ultrasonic sensor sketch is currently required or committed.

The Arduino Uno is currently used as the TB6600 motor pulse and direction controller. Keep future Arduino sensor-interface code here only if the hardware architecture changes and sensors are deliberately moved to the Arduino.

Document any future serial message format, pin assignments, sampling rate, and error handling before integrating it with the Raspberry Pi.