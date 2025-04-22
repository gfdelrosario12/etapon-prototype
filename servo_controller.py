import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 1000)  # Pin 18, 1kHz frequency
pwm.start(50)            # Start PWM with 50% duty cycle

time.sleep(2)

pwm.ChangeDutyCycle(75)  # Change duty cycle to 75%
time.sleep(2)

pwm.stop()
GPIO.cleanup()

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
