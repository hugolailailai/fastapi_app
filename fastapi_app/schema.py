# schemas.py
from typing import List
from pydantic import BaseModel, Field
#from uuid import UUID
from datetime import datetime


class Order_Item_Base(BaseModel):
    id: int
    order_id: int
    product_name: str
    amount: int
    product_id: int
    price: int

    class Config:
        orm_mode = True


class Order_Base(BaseModel):
    id: int
    customer_name: str
    customer_id: str
    purchase_time: datetime
    order_item: List[Order_Item_Base]

    class Config:
        orm_mode = True
