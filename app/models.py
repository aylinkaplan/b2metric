from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)

    # Relationships
    transactions = relationship("Transaction", back_populates="book")


class Patron(Base):
    __tablename__ = "patron"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

    # Relationships
    transactions = relationship("Transaction", back_populates="patron")


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    patron_id = Column(Integer, ForeignKey("patron.id"), nullable=False)
    checkout_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    # Relationships
    book = relationship("Book", back_populates="transactions")
    patron = relationship("Patron", back_populates="transactions")
