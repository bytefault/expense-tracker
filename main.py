from flask import Flask, render_template, request, redirect, session
import mysql.connector  # pyright: ignore[reportMissingImports]
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4321",
    database="mydb"
)
cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation',  methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cursor.fetchall()
    print(users)
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)