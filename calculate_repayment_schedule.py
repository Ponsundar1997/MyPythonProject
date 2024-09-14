Python
from config import engine
from sqlalchemy import text, create_engine
from sqlalchemy.engine import reflection
import pandas as pd

def calculate_loan_repayment(loan_id):
    # Connect to the database
    conn = engine.connect()

    # Calculate loan repayment
    loan_amount = None
    interest_rate = None
    loan_term = None
    start_date = None
    monthly_interest_rate = None
    monthly_payment = None
    balance = None
    principal_amount = None
    interest_amount = None
    payment_date = None

    # Get loan details
    conn.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), loan_id={'loan_id': loan_id}).fetchall()

    for row in conn.statement.execute(conn.statement.params).fetchall():
        loan_amount, interest_rate, loan_term, start_date = row

    monthly_interest_rate = interest_rate / 100 / 12

    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-loan_term))
    balance = loan_amount
    payment_date = start_date

    # Initialize payment number
    payment_number = 1

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        interest_amount = balance * monthly_interest_rate
        principal_amount = monthly_payment - interest_amount
        balance = balance - principal_amount

        # Define the insert query
        insert_query = text("""
            INSERT INTO repaymentschedule 
            (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
            VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
        """)

        # Execute the insert query
        conn.execute(insert_query, loan_id=loan_id, payment_number=payment_number, payment_date=payment_date, principal_amount=principal_amount, interest_amount=interest_amount, monthly_payment=monthly_payment, balance=balance)

        payment_date = payment_date + pd.DateOffset(months=1)
        payment_number += 1

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
