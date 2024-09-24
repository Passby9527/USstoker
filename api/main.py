import os
from flask import Flask
from database import create_session_maker, USStock

app = Flask(__name__)
DB_CONNECTION_STRING = os.environ["DB_CONNECTION_STRING"]


@app.get("/")
def list_stock_infos():
    session = create_session_maker(DB_CONNECTION_STRING)()
    try:
        results = session.query(
            USStock.stock_symbol,
            USStock.date,
            USStock.close_price,
        ).all()
        return [
            {
                "stock_symbol": r.stock_symbol,
                "date": r.date,
                "close_price": r.close_price,
            }
            for r in results
        ]
    finally:
        session.close()
