import os
from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

app = Flask(__name__)
DB_PATH = os.environ["DB_PATH"]

# 創建 SQLAlchemy 引擎
engine = create_engine(f"sqlite:///{DB_PATH}", poolclass=NullPool)

# 創建 sessionmaker
Session = sessionmaker(bind=engine)

# 創建 declarative base
Base = declarative_base()


# 定義模型
class USStock(Base):
    __tablename__ = "us_stock"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    date = Column(String)
    close_price = Column(Float)


# 創建資料庫表格（如果不存在）
Base.metadata.create_all(engine)


@app.get("/")
def list_stock_infos():
    session = Session()
    try:
        results = session.query(USStock.code, USStock.date, USStock.close_price).all()
        return [
            {"code": r.code, "date": r.date, "close_price": r.close_price}
            for r in results
        ]
    finally:
        session.close()
