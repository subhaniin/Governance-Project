from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Use a secure random key in production

# DB Config (update as per your PostgreSQL setup)
conn = psycopg2.connect(
    host="localhost",
    dbname="governance",
    user="postgres",
    password="Pqsql"
)

@app.route('/')
def home():
    return render_template('base.html')  # Placeholder

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect and query database
        cur = conn.cursor()
        cur.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            return f"Welcome Admin {username}"
        else:
            return "Invalid credentials!"
    return render_template('login_admin.html')


@app.route('/citizen_login', methods=['GET', 'POST'])
def citizen_login():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        # Check citizen name and DOB from DB here
        return f"Welcome Citizen {name}"
    return render_template('login_citizen.html')


if __name__ == '__main__':
    app.run(debug=True)
