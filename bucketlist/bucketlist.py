# all the imports
import os

from flask import Flask, request, json, session, g, redirect, url_for, abort, \
     render_template, flash

from flask.ext.mysql import MySQL

# from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__) # create the application instance :)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route("/")
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    conn = mysql.connect()

    # Cursor is used to query stored procedure in MySQL
    cursor = conn.cursor()


    # validate the received values
    if _name and _email and _password:
        # _hashed_password = generate_password_hash(_password)
        _hashed_password = _password

        # calling stored procedure of MySQL
        cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})

        # return json.dumps({'html': '<span>All fields good !!</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})
