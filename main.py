from flask import Flask, render_template, redirect, url_for, request, make_response, Response
from utils.servoFunction import servoFunction
from utils.camera import Camera
from utils.jwtVerifier import fluxJwtVerifier, cookieJwtVerifier
from threading import Semaphore
import os
import json
import jwt

buttonSem = Semaphore(1)

app = Flask(__name__)

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@app.route('/flux')
def flux():
    if fluxJwtVerifier(request):
        buttonDisabled = False if buttonSem._value == 1 else True
        return render_template('flux.html', buttonDisabled=buttonDisabled)
    else: 
        return redirect(url_for('login'))

@app.route('/opendoor', methods=['POST']) 
def opendoor():
    if fluxJwtVerifier(request):
        if buttonSem._value == 1:
            buttonSem.acquire()
            servoFunction()
            buttonSem.release()
            return redirect(url_for('flux'))
        else:
           return redirect(url_for('flux')) 
    else: 
        return redirect(url_for('login'))

@app.route('/setcookie', methods=['GET', 'POST'])
def setCookie():
    if cookieJwtVerifier(request):
        resp = make_response(redirect('/flux'))
        resp.set_cookie('jwt', request.args.get('encodedJwt'), max_age=43200)
        return resp
    return redirect(url_for('login'))
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        jsonFile = open(f"{os.path.dirname(os.path.abspath(__file__))}\\users.json")
        userJson = json.load(jsonFile)
        if request.form['username'] in userJson:
            targetedUser = userJson.get(request.form['username'])
            if request.form['password'] == targetedUser.get("password"):
                encodedJwt = jwt.encode({"username": request.form['username']}, "elhuevo", algorithm="HS256")
                return redirect(url_for('setCookie', username=request.form['username'], encodedJwt=encodedJwt, method='POST'))
            else:
                error = 'Invalid Credentials. Please try again.'
        else:
                error = 'Invalid Credentials. Please try again.' 
    if fluxJwtVerifier(request):
        return redirect(url_for('flux'))
    return render_template('login.html', error=error)

@app.route('/video_feed')
def video_feed():
    if fluxJwtVerifier(request):
        return Response(gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else: 
        return redirect(url_for('login'))

@app.route('/')
def index():
    if fluxJwtVerifier(request):
        return redirect(url_for('flux'))
    else: 
        return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')