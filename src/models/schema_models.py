from typing import List

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, Integer, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from datetime import datetime

class Base(DeclarativeBase):
    pass


user_group_association = Table(
    "user_group_association",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(String(60))
    users: Mapped[List[User]] = relationship(secondary=user_group_association)
    
    
class ExpenseBreakDown(Base):
    __tablename__ = "expense_breakdowns"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"))
    payer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column(Integer)
    is_settled: Mapped[bool] = mapped_column(Boolean, default=False)
    
    def __repr__(self) -> str:
        return f"ExpenseBreakDown(id={self.id}, expense_id={self.expense_id}, \
            payer_id={self.payer_id}, receiver_id={self.receiver_id}, amount={self.amount}, is_settled={self.is_settled})"
    

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    description: Mapped[str] = mapped_column(String(60))
    date: Mapped[datetime] = mapped_column(DateTime)
    total_amount: Mapped[int] = mapped_column(Integer)
    expense_breakdowns: Mapped[List[ExpenseBreakDown]] = relationship(cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"Expense(id={self.id}, creator_id={self.creator_id}, \
            group_id={self.group_id}, description={self.description}, \
            date={self.date}, total_amount={self.total_amount}, \
            )"
