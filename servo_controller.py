import RPi.GPIO as GPIO
import time

# Define GPIO pins
BIO_SERVO_PIN = 17
NONBIO_SERVO_PIN = 27

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BIO_SERVO_PIN, GPIO.OUT)
GPIO.setup(NONBIO_SERVO_PIN, GPIO.OUT)

# Initialize PWM at 50Hz
bio_pwm = GPIO.PWM(BIO_SERVO_PIN, 50)
nonbio_pwm = GPIO.PWM(NONBIO_SERVO_PIN, 50)
bio_pwm.start(0)
nonbio_pwm.start(0)

def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 180.0) * 10  # maps angle (0–180) to 2.5–12.5 duty

def move_servo(pwm):
    for angle in range(0, 181, 5):
        pwm.ChangeDutyCycle(angle_to_duty_cycle(angle))
        time.sleep(0.01)
    for angle in range(180, -1, -5):
        pwm.ChangeDutyCycle(angle_to_duty_cycle(angle))
        time.sleep(0.01)
    pwm.ChangeDutyCycle(0)

def move_biodegradable_servo():
    move_servo(bio_pwm)

def move_nonbiodegradable_servo():
    move_servo(nonbio_pwm)

def cleanup():
    bio_pwm.stop()
    nonbio_pwm.stop()
    GPIO.cleanup()
