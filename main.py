from flask import Flask
import RPi.GPIO as GPIO
import time

SERVO_PIN = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)
p = GPIO.PWM(SERVO_PIN ,50)

app = Flask(__name__) 
@app.route('/')
def index():
    p.start(2.5)
    time.sleep(2)
    p.ChangeFrequency(10)
    time.sleep(2)
    p.ChangeFrequency(2.5)
    time.sleep(2)
    p.stop()
    return "Hello world"
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')