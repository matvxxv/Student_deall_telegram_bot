from sqlalchemy import Column, Integer, VARCHAR, Boolean, DateTime, Float, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import declarative_base


BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)     # Telegram user id
    username = Column(VARCHAR(32))
    reg_date = Column(DateTime, nullable=False, default=datetime.now())
    last_visit_date = Column(DateTime, nullable=False, onupdate=datetime.now(), default=datetime.now())
    is_executor = Column(Boolean, nullable=False, default=False)
    completed_orders = Column(Integer, nullable=False, default=0)
    feedback_num = Column(Integer, nullable=False, default=0)
    ranking = Column(Float, nullable=False, default=0)
    total_cash_spent = Column(Float, nullable=True)
    total_cash_get = Column(Float, nullable=True)

    def __str__(self) -> str:
        return f'<User: {self.user_id}>'

class Order(BaseModel):
    __tablename__ = 'orders'

    order_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    executor_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    subject = Column(VARCHAR(64), nullable=False)
    photo_id = Column(VARCHAR(256), nullable=True)
    order_date = Column(DateTime, nullable=False, default=datetime.now())
    price = Column(Float, nullable=True)
    comment = Column(Text, nullable=False)






