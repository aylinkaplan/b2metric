from datetime import datetime, timedelta

from app.celery_config import celery_app
from app.database import SessionLocal
from app.models import Transaction, Patron


@celery_app.task
def send_overdue_reminders():
    db = SessionLocal()
    current_date = datetime.now().date()
    overdue_transactions = db.query(Transaction).filter(Transaction.return_date == None,
                                                        Transaction.checkout_date < current_date).all()

    for transaction in overdue_transactions:
        patron = db.query(Patron).filter(Patron.id == transaction.patron_id).first()
        if patron:
            # Send an email
            send_email(patron.email, "Overdue Book Reminder", f"Your book '{transaction.book.title}' is overdue.")

    db.close()


@celery_app.task
def generate_weekly_reports():
    db = SessionLocal()
    current_date = datetime.now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())  # Start of the current week
    end_of_week = start_of_week + timedelta(days=7)  # End of the current week

    checked_out_books_count = db.query(Transaction).filter(Transaction.return_date == None, Transaction.checkout_date.between(start_of_week, end_of_week)).count()

    # Generate and send a report
    generate_report(checked_out_books_count)
    db.close()


def send_email(to_email, subject, body):
    print(f"Sending email to {to_email} with subject '{subject}' and body '{body}'")
    pass


def generate_report(checked_out_books):
    print(f"Weekly report: {checked_out_books} books are currently checked out.")
    pass
