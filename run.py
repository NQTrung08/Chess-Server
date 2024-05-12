import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="chess_local",
)


if __name__ == "__main__":
    app.run(debug=True)
