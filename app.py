from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import pymysql
import re
import bcrypt

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = "Secret Key"
pymysql.install_as_MySQLdb()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:yourpassword@localhost/nameofdatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, userName, email, password):
        self.userName = userName
        self.email = email
        self.password = password

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password'].encode("utf-8")
        email = request.form['email']

        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        account = Data1.query.filter_by(email=email).first()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            new_user = Data1(userName, email, hash_password)
            db.session.add(new_user)
            db.session.commit()
            message = 'You have successfully registered!'

    elif request.method == 'POST':
        message = 'Please fill out the form!'

    return render_template('register.html', message=message)

@app.route("/login", methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = Data1.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            session['loggedin'] = True
            session['userid'] = user.id
            session['name'] = user.userName
            session['email'] = user.email
            message = 'Logged in successfully!'
            return render_template('loggedin.html', message=message)
        else:
            message = 'Please enter correct email/password!'

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/ide_page')
def ide_page():
    return render_template('IDE.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    code = request.form['code']
    return jsonify({'output': code})

if __name__ == "__main__":
    app.run(debug=True)
