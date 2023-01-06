import RPi.GPIO as GPIO
import time

SERVO_PIN = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)
p = GPIO.PWM(SERVO_PIN, 50)

def servoFunction():
    p.start(2.5)
    time.sleep(2)
    p.ChangeFrequency(7.5)
    time.sleep(2)
    p.ChangeFrequency(10)
    time.sleep(2)
    p.ChangeFrequency(7.5)
    time.sleep(2)
    p.ChangeFrequency(2.5)
    time.sleep(2)
    p.stop()