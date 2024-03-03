from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

def insertVolunteer(firstName, lastName, email, phoneNumber, address):
    database = "volunteer.db"
    tablename = "volunteers"
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("INSERT INTO volunteers (first_name, last_name, email, phone_number, address) VALUES (?,?,?,?,?)", (firstName, lastName, email, phoneNumber, address))
    con.commit()
    con.close()

def retrieveVolunteer():
    database = "volunteer.db"
    tablename = "volunteer"
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM volunteers")
    volunteers = cur.fetchall()
    con.close()
    return volunteers

def createConnection(dbFile):
    connection = None
    try:
        conn = sqlite3.connect(dbFile, check_same_thread=False)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

if __name__ == '__main__':
    conn = createConnection("volunteer.db")
    c = conn.cursor()

def createTable(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS volunteers (id INTEGER PRIMARY_KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL, phone_number TEXT NOT NULL, address TEXT NOT NULL)")
    conn.commit()
    return c.lastrowid

def main():
    database = r"volunteer.db"
    conn = createConnection(database)
    c = conn.cursor()

    if conn is not None:
        createTable(conn)
    else:
        print("Error. Cannot create the database connection.")

if __name__ == '__main__':
    main()

@app.route('/')
def index():
    return render_template("volunteer_form.html")

@app.route('/my_form', methods = ['POST', 'GET'])
def my_form():
    if request.method == 'POST': 
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        email = request.form['email']
        phoneNumber = request.form['phone_number']
        address = request.form['address']
    
    try:
        insertVolunteer(firstName, lastName, email, phoneNumber, address)
        volunteers = retrieveVolunteer()
        return render_template("volunteer_form.html", volunteers = volunteers)
    except:
        return "Something went wrong while saving the data"
    
if __name__ == '__main__':
    app.run(debug = True)

        
