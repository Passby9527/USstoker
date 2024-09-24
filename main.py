import os
import sys

import pandas as pd

import crawl
from database import DB

def stock_list_parser(file_path):
    with open(file_path,'r')as f:
        stock_list = f.read().split('\n')
    return stock_list
file_path = os.path.join(os.getcwd(), 'stock_list.txt')
stock_list = stock_list_parser(file_path)

if __name__ == "__main__":
    # crawl
    df = pd.DataFrame()
    for stock in stock_list:
        data = crawl.crawl_cnyes(stock)
        df = pd.concat([df, pd.DataFrame([data])])

    file_path = os.path.join(os.getcwd(), 'tmp_data.csv')
    df.to_csv(file_path, index=False)

    # insert into sqlite
    CONFIG_PATH = os.path.join(os.getcwd(), "DB_CONFIG.json")
    db = DB(CONFIG_PATH, "sqlite")
    data = pd.read_csv(file_path).to_dict('records')
    
    # Insert
    response = db.create_stocks(data)
    print(response)