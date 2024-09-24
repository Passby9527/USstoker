from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 創建 declarative base
Base = declarative_base()


# 定義模型
class USStock(Base):
    __tablename__ = "us_stock"

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String)
    date = Column(String)
    close_price = Column(Float)


def create_session_maker(connection_string):
    # 創建 SQLAlchemy 引擎
    engine = create_engine(connection_string, poolclass=NullPool)

    # 創建資料庫表格（如果不存在）
    Base.metadata.create_all(engine)

    # 創建 sessionmaker
    Session = sessionmaker(bind=engine)

    return Session
