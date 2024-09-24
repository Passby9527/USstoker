import os
import json

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def json_parser(file_path):
    with open(file_path, 'r')as f:
        return json.loads(f.read())

# create statement
def create_db_url(config):
    drivername = config['drivername']
    database = config['database']
    username = config['username']
    password = config['password']
    host = config['host']
    port = config['port']
    
    if drivername == 'sqlite':
        return f"{drivername}:///{database}"
    else:
        return f"{drivername}://{username}:{password}@{host}:{port}/{database}"

# create engine
def create_db_engine(CONFIG_PATH, db_name):
    config = json_parser(CONFIG_PATH)[db_name]
    engine = create_engine(create_db_url(config), echo=True)
    return engine

# def create_db_schema():
#     return schema

Base = declarative_base()
# define model class
class USStock(Base):
    __tablename__ = 'us_stock'
    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String)
    date = Column(String)
    close_price = Column(Float)

    def __repr__(self):
        return f"<USStock(stock_symbol='{self.stock_symbol}', close_price='{self.close_price}', date='{self.date}')>"

# create session
def create_db_session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class DB:
    def __init__(self, CONFIG_PATH, db_name):
        engine = create_db_engine(CONFIG_PATH, db_name)
        self.session = create_db_session(engine)

    # CRUD
    def create_stock(self, stock_symbol, date, close_price):
        new_stock = USStock(stock_symbol=stock_symbol, date=date, close_price=close_price)
        self.session.add(new_stock)
        self.session.commit()
        return new_stock

    def create_stocks(self, stocks):
        # stock = {"stock_symbol":stock_symbol, "date":date, "close_price":close_price}
        # stocks = [{stock_1}, {stock_2}]
        stocks_object = [
            USStock(
                stock_symbol=stock['stock_symbol'], 
                date=stock['date'], 
                close_price=stock['close_price']
                ) for stock in stocks
                ]
        self.session.add_all(stocks_object)
        self.session.commit()
        return stocks_object

    def read_stock(self, stock_id):
        data = self.session.query(USStock).filter(USStock.id == stock_id).first()
        return data 

    def read_all_stocks(self):
        data = self.session.query(USStock).all()
        return data

    def update_stock(self, stock_id, stock_symbol=None, date=None, close_price=None):
        stock = self.session.query(USStock).filter(USStock.id == stock_id).first()
        if stock:
            if stock_symbol:
                stock.stock_symbol = stock_symbol
            if date:
                stock.date = date
            if close_price:
                stock.close_price = close_price
            self.session.commit()
        return stock

    def delete_stock(self, stock_id):
        stock = self.session.query(USStock).filter(USStock.id == stock_id).first()
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False

# test
if __name__ == "__main__":
    CONFIG_PATH = os.path.join(os.getcwd(), "DB_CONFIG.json")
    db = DB(CONFIG_PATH, "sqlite")
    
    test_data_1 = {"stock_symbol":"XD", "date":"Hello, 12/27", "close_price": 95.27}
    test_data_2 = {"stock_symbol":"==", "date":"Hello, 12/28", "close_price": 19.76}
    
    # create
    #response = db.create_stock(**test_data_1)
    
    # read
    #response = db.read_all_stocks()

    #update
    # response = db.update_stock(1, **test_data_2)

    #delete
    response = db.delete_stock(2)
    print("=======================")
    print(response)
