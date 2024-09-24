import os
import sqlite3
from flask import Flask, g

app = Flask(__name__)

DB_PATH = os.environ["DB_PATH"]


def get_connection():
    connection = getattr(g, "_connection", None)

    if connection is None:
        connection = g._connection = sqlite3.connect(DB_PATH)

    return connection


@app.get("/")
def list_stock_infos():
    connection = get_connection()
    cursor = connection.cursor()
    result = cursor.execute("SELECT code, date, close_price FROM us_stock")

    return result.fetchall()
