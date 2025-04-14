from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from db_config import db

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']

    try:
        cursor = db.cursor()
        sql = "SELECT name FROM users WHERE email=%s AND password=%s"
        cursor.execute(sql, (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = user[0]
            return redirect(url_for('welcome'))
        else:
            flash("Error de credenciales")
            return redirect(url_for('login_page'))
    except Exception as e:
        flash("Error de credenciales")
        return redirect(url_for('login_page'))

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)


