import pyodbc
from flask import Flask, render_template, request, redirect, url_for, session

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=KPC129\\PruebaJT;'
        'DATABASE=PersonalProjects;'
        'UID=sa;'
        'PWD=PruebaJT12345'
    )
    return conn

appTracker = Flask(__name__)

@appTracker.route('/')
def tracker():
    return render_template('Tracker.html')

if __name__=='__main__':
    appTracker.run(debug=True)