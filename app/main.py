from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, schemas
from datetime import datetime

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new book
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Get all books
@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


# Create a new patron
@app.post("/patrons/", response_model=schemas.Patron)
def create_patron(patron: schemas.PatronCreate, db: Session = Depends(get_db)):
    db_patron = models.Patron(**patron.dict())
    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron


# Get all patrons
@app.get("/patrons/", response_model=list[schemas.Patron])
def read_patrons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    patrons = db.query(models.Patron).offset(skip).limit(limit).all()
    return patrons


# Check out a book
@app.post("/transactions/checkout/", response_model=schemas.Transaction)
def checkout_book(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == transaction.book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db.query(models.Transaction).filter(
            models.Transaction.book_id == transaction.book_id,
            models.Transaction.return_date.is_(None)).first():
        raise HTTPException(status_code=400, detail="Book is already checked out")

    db_transaction = models.Transaction(
        book_id=transaction.book_id,
        patron_id=transaction.patron_id,
        checkout_date=datetime.utcnow(),
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# Return a book
@app.post("/transactions/return/", response_model=schemas.Transaction)
def return_book(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

    if not db_transaction or db_transaction.return_date is not None:
        raise HTTPException(status_code=404, detail="Transaction not found or book already returned")

    db_transaction.return_date = datetime.utcnow()
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# Get all transactions
@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions


# List all checked-out books
@app.get("/books/checked-out/", response_model=list[schemas.Book])
def read_checked_out_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).filter(models.Transaction.return_date.is_(None)).offset(skip).limit(
        limit).all()
    book_ids = [transaction.book_id for transaction in transactions]
    books = db.query(models.Book).filter(models.Book.id.in_(book_ids)).all()
    return books


# List all overdue books (simplified for demo purposes)
@app.get("/books/overdue/", response_model=list[schemas.Book])
def read_overdue_books(db: Session = Depends(get_db)):
    overdue_date = datetime.utcnow()  # Modify as needed to determine what qualifies as overdue
    transactions = db.query(models.Transaction).filter(
        models.Transaction.return_date.is_(None),
        models.Transaction.checkout_date < overdue_date).all()

    book_ids = [transaction.book_id for transaction in transactions]
    books = db.query(models.Book).filter(models.Book.id.in_(book_ids)).all()
    return books
