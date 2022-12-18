from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
#from uuid import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Order(Base):
    # create __tablename__ attribute，宣告 model 對應的 database table name
    __tablename__ = "order"
    # create class attribute，宣告 model 對應的 table field/column
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_id = Column(String)
    purchase_time = Column(DateTime(timezone=True), server_default=func.now())
    # create relationship 建立 Table 關聯
    order_item = relationship("Order_Item", back_populates="order")


class Order_Item(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_name = Column(String)
    amount = Column(Integer)
    product_id = Column(Integer)
    price = Column(Integer)
    # create relationship
    order = relationship("Order", back_populates="order_item")
