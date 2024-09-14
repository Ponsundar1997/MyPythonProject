
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import engine
import pandas as pd

def calculate_repayment_schedule(loan_id):
    # Create a session from the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Retrieve loan details
    loan_details = session.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), params={"loan_id": loan_id}).fetchone()
    loan_amount, interest_rate, loan_term, start_date = loan_details

    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Create a list to store the repayment schedule
    repayment_schedule = []

    # Iterate through each month and calculate the repayment schedule
    for payment_number in range(1, loan_term + 1):
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Add the repayment details to the list
        repayment_schedule.append({
            "paymentnumber": payment_number,
            "paymentdate": payment_date,
            "principalamount": principal_amount,
            "interestamount": interest_amount,
            "totalpayment": monthly_payment,
            "balance": balance
        })

        # Move to the next month
        payment_date += pd.Timedelta(days=30)  # Assume 30-day months

    # Create a DataFrame from the repayment schedule list
    df = pd.DataFrame(repayment_schedule)

    # Execute the DDL command to create the RepaymentSchedule table
    engine.execute(text("CREATE TABLE IF NOT EXISTS repaymentschedule (loanid INTEGER, paymentnumber INTEGER, paymentdate DATE, principalamount DECIMAL(15, 2), interestamount DECIMAL(15, 2), totalpayment DECIMAL(15, 2), balance DECIMAL(15, 2))"))

    # Insert the repayment schedule into the RepaymentSchedule table
    df.to_sql("repaymentschedule", engine, if_exists="append", index=False, chunksize=1000)

    return df

loan_id = 123
df = calculate_repayment_schedule(loan_id)
