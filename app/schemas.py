from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class BookBase(BaseModel):
    title: str
    author: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PatronBase(BaseModel):
    name: str
    email: str


class PatronCreate(PatronBase):
    pass


class Patron(PatronBase):
    id: int
    books: List[Book] = []

    model_config = ConfigDict(from_attributes=True)


class TransactionBase(BaseModel):
    book_id: int
    patron_id: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    checkout_date: datetime
    return_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
