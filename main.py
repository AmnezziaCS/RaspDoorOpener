from flask import Flask, render_template, redirect, url_for, request, make_response, Response
from servoFunction import servoFunction
from camera import Camera

app = Flask(__name__)

@app.route('/flux')
def flux():
    if request.cookies.get('userID'):
        return render_template('flux.html')
    return "Access denied"

@app.route('/opendoor', methods=['POST']) 
def opendoor():
    servoFunction()
    return redirect(url_for('flux'))

@app.route('/setcookie', methods=['GET', 'POST'])
def setCookie():
    resp = make_response(redirect('/flux'))
    resp.set_cookie('userID', request.form['username'])
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('flux'))
    return render_template('login.html', error=error)

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    if request.cookies.get('userID'):
        return redirect(url_for('flux'))
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')