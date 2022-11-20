import datetime
from app import app
from config import mysql
from flask_mail import Mail, Message
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import json

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aqmal.dev81@gmail.com'
app.config['MAIL_PASSWORD'] = 'uglkauqrofjtkaac'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/home')
def home():
    if 'email' in session:
        email = session['email']
        return jsonify({'message' : 'You are already logged in', 'email' : email})
    else:
        resp = jsonify({'message' : 'Unauthorized'})
        resp.status_code = 401
        return resp

@app.route('/signin', methods=['POST'])
def signin():
    try:
        _json = request.json
        _email = _json['email']
        _password = _json['password']
        if _email and _password and request.method == 'POST':
            sql = "SELECT * FROM `user` WHERE `email`=%s"
            data = (_email)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            email = rows['email']
            password = rows['password']
            if rows:
                if check_password_hash(password, _password):
                    session['email'] = email
                    cursor.close()
                    connection.close()
                    response = jsonify('Sign in Success')
                    response.status_code = 200
                else:
                    response = jsonify('Wrong password')
                    response.status_code = 400
            else:
                response = jsonify('User not found')
                response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Failed to sign in')
        response.status_code = 400
    finally:
        return response

@app.route('/signout')
def signout():
    if 'email' in session:
        session.pop('email', None)
        resp = jsonify({'message' : 'You have successfully logged out'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message' : 'Unauthorized'})
        resp.status_code = 401
        return resp

@app.route('/signup', methods=['POST'])
def signup():
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['password']
        _reg_type = _json['reg_type']
        if _name and _email and _password and request.method == 'POST':
            sql = "INSERT INTO `user` (`email`,`password`,`reg_type`,`name`) VALUES (%s,%s,%s,%s)"
            data = (_email, generate_password_hash(_password), _reg_type, _name)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            print(cursor._last_executed)
            user_id = cursor.lastrowid
            if _reg_type == 1:
                sql = "INSERT INTO `mentor_main` (`name`, `email`, `user_id`) VALUES (%s,%s,%s)"
                data = (_name, _email, user_id)
                cursor.execute(sql, data)
            elif _reg_type == 2:
                sql = "INSERT INTO `individual_main` (`name`, `email`, `user_id`) VALUES (%s,%s,%s)"
                data = (_name, _email, user_id)
                cursor.execute(sql, data)
            elif _reg_type == 3:
                sql = "INSERT INTO `business_main` (`name`, `email`, `user_id`) VALUES (%s,%s,%s)"
                data = (_name, _email, user_id)
                cursor.execute(sql, data)
            else:
                response = jsonify('Invalid registration type')
                response.status_code = 400
            connection.commit()
            cursor.close()
            connection.close()
            response = jsonify('User has been registered successfully')
            response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to register user')
        response.status_code = 400
    finally:
        return response

@app.route('/resetPassword', methods=['POST'])
def resetPassword():
    try:
        _json = request.json
        _email = _json['email']
        if _email and request.method == 'POST':
            sql = "SELECT * FROM `user` WHERE `email`=%s"
            data = (_email)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            email = rows['email']
            if rows:
                msg = Message('Reset Password', sender = 'aqmal.dev81@gmail.com', recipients = [email])
                msg.body = "reset password"
                mail.send(msg)
                cursor.close()
                connection.close()
                response = jsonify('Email sent')
                response.status_code = 200
            else:
                response = jsonify('User not found')
                response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Failed to send email')
        response.status_code = 400
    finally:
        return response

@app.route('/confirmResetPassword', methods=['PUT'])
def confirmResetPassword():
    try:
        _json = request.json
        _email = _json['email']
        _password = _json['password']
        _confirmPassword = _json['confirmPassword']
        if _email and _password and request.method == 'POST':
            sql = "SELECT * FROM `user` WHERE `email`=%s"
            data = (_email)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            email = rows['email']
            if rows:
                if _password == _confirmPassword:
                    hashed_password = generate_password_hash(_password)
                    sql = "UPDATE `user` SET `password`=%s WHERE `email`=%s"
                    data = (hashed_password, _email)
                    cursor.execute(sql, data)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    response = jsonify('Password changed')
                    response.status_code = 200
                else:
                    response = jsonify('Password not match')
                    response.status_code = 400
            else:
                response = jsonify('User not found')
                response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Failed to change password')
        response.status_code = 400
    finally:
        return response


if __name__ == "__main__":
    app.run(debug=True)