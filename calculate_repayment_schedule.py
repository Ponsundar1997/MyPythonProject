Python
from config import engine
from sqlalchemy import text, Interval
import pandas as pd

def calculate_repayment_schedule(loan_id):
    # Translate PostgreSQL query to SQLAlchemy SQL expression
    query = text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id;
    """)

    # Execute the query and fetch the result
    result = engine.execute(query, loan_id=loan_id).fetchone()

    if result is None:
        return None

    loan_amount, interest_rate, loan_term, start_date = result

    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = (interest_rate / 100 / 12)

    # Calculate fixed monthly payment
    monthly_payment = (loan_amount * monthly_interest_rate) / \
                       (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize variables
    balance = loan_amount
    payment_date = start_date
    payment_number = 1

    # Repayment schedule
    repayment_schedule = []

    while payment_number <= loan_term:
        # Calculate interest and principal for the current month
        interest_amount = balance * monthly_interest_rate
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Insert repayment details into the repayment schedule
        repayment_schedule.append({
            'loanid': loan_id,
            'paymentnumber': payment_number,
            'paymentdate': payment_date,
            'principalamount': principal_amount,
            'interestamount': interest_amount,
            'totalpayment': monthly_payment,
            'balance': balance
        })

        # Move to the next month
        payment_date += Interval(days=30)
        payment_number += 1

    # Create a DataFrame from the repayment schedule
    df = pd.DataFrame(repayment_schedule)

    return df
