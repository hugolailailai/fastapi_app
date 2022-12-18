import os
import uvicorn
from dotenv import load_dotenv
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Order, Order_Item
from schema import Order_Base, Order_Item_Base

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/order-item/add/", response_model=Order_Item_Base)
def create_order_item(order_item: Order_Item_Base):
    db_orderitem = Order_Item(
        order_id=order_item.order_id,
        product_name=order_item.product_name,
        amount=order_item.amount,
        product_id=order_item.product_id,
        price=order_item.price
    )
    db.session.add(db_orderitem)
    db.session.commit()
    return db_orderitem


@app.get('/order-item/list/', response_model=Order_Item_Base)
def list_orders():
    order_items = db.session.query(Order_Item).all()
    return order_items


@app.post('/order/add/', response_model=Order_Base)
def create_order(order: Order_Base):
    db_order = Order(
        customer_name=order.customer_name,
        customer_id=order.customer_id,
        purchase_time=order.purchase_time,
        order_item=order.order_item
    )
    db.session.add(db_order)
    db.session.commit()
    return db_order


@app.get('/order/list/', response_model=Order_Base)
def list_orders():
    orders = db.session.query(Order).all()
    return orders


@app.get('/order/list/{order_id}', response_model=Order_Base)
def get_order(order_id: int):
    return db.session.query(Order).filter(Order.id == order_id).first()


@app.put('/order/modify/{order_id}', response_model=Order_Base)
def update_order(order_id: int, order: Order_Base):
    db_order = get_order(order_id=order_id)
    if not db_order:
        raise HTTPException(
            status_code=404,
            detail=f'order_id: {order_id} does not exist.'

        )
    db_order.update(order.dict())
    return f'updated {order_id}'
