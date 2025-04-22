import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
BIO_PIN = 8
NONBIO_PIN = 9

# Setup PWM pins
GPIO.setup(BIO_PIN, GPIO.OUT)
GPIO.setup(NONBIO_PIN, GPIO.OUT)

# Start PWM at 50Hz (standard for servos)
bio_pwm = GPIO.PWM(BIO_PIN, 50)
nonbio_pwm = GPIO.PWM(NONBIO_PIN, 50)

bio_pwm.start(0)
nonbio_pwm.start(0)

# Map angle (0–180) to 2.5–12.5% duty cycle (for 500–2500 µs pulse width)
def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 180.0) * 10

# Generic servo movement function
def move_servo(pwm):
    for angle in range(5, 151, 1):
        pwm.ChangeDutyCycle(angle_to_duty_cycle(angle))
        time.sleep(0.02)
    for angle in range(150, 4, -1):
        pwm.ChangeDutyCycle(angle_to_duty_cycle(angle))
        time.sleep(0.02)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)

# Individual control functions
def move_biodegradable_servo():
    move_servo(bio_pwm)

def move_nonbiodegradable_servo():
    move_servo(nonbio_pwm)

# Optional: test run both
if __name__ == "__main__":
    try:
        move_biodegradable_servo()
        move_nonbiodegradable_servo()
    finally:
        bio_pwm.stop()
        nonbio_pwm.stop()
        GPIO.cleanup()
