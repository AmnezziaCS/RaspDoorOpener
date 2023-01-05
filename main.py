from flask import Flask, render_template, redirect, url_for, request, make_response
import time

app = Flask(__name__)

@app.route('/flux')
def flux():
    if request.cookies.get('userID'):
        return render_template('flux.html')

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

@app.route('/')
def index():
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')