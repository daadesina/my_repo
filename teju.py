#!/usr/bin/env python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, url_for, request, redirect

basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)

app.config["SECRET_KEY"] = 'secrete_key'
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


with app.app_context():
	db.create_all()
	
main = Blueprint('main', __name__)
main_blueprint = main
app.register_blueprint(main_blueprint)
    


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    other_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))



    

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up_post():

    global sign_up_email
    global sign_up_password
    sign_up_fname = request.form.get('fname')
    sign_up_oname = request.form.get('oname')
    sign_up_lname = request.form.get('lname')
    sign_up_email = request.form.get('email')
    sign_up_password = request.form.get('password')

    unique_email = User.query.filter_by(email=sign_up_email).first()

    if unique_email:
        print ("The Email has already been registered")
        return redirect(url_for('main.sign_up'))

    new_user = User(
            first_name=sign_up_fname, 
            other_name=sign_up_oname, 
            last_name=sign_up_lname, 
            email=sign_up_email, 
            password=bcrypt.generate_password_hash(sign_up_password).decode('utf-8')
            )

    db.session.add(new_user)
    db.session.commit()


    return redirect(url_for('main.login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=["GET", "POST"])
def login_post():
    logged_in = True

    login_email = request.form.get('email')
    login_password = request.form.get('password')

    check_email = User.query.filter_by(email=login_email).first()

    if check_email:
        check_password = check_email.password
    else:
        print("Wrong Email !!!")
        return redirect(url_for('login'))

    if bcrypt.check_password_hash(check_password, login_password):
        return redirect(url_for('index'))
    else:
        print("Wrong Password !!!")
        return redirect(url_for('login'))
        
@app.route('/index')
def index():
    return render_template('index.html')
    






@app.route('/')
def home():
    return render_template('login.html')

@app.route('/nature')
def art():
    return render_template('nature.html')



@app.route('/language')
def language():
    return render_template('language.html')

@app.route('/culture')
def culture():
    return render_template('culture.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/africa')
def news():
    return render_template('africa.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
