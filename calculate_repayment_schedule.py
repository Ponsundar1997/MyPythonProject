Python
from config import engine
from sqlalchemy import text
import pandas as pd

def calculate_repayment_schedule(loan_id):
    conn = engine.connect()

    # Get loan details
    result = conn.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), loan_id=loan_id)
    loan_details = result.fetchone()
    loan_amount, interest_rate, loan_term, start_date = loan_details

    # Convert annual interest rate to monthly interest rate (divide by 12)
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # List to store the repayment details
    repayments = []

    # Loop through each month and calculate the repayment schedule
    for i in range(1, loan_term + 1):
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Insert repayment details into the RepaymentSchedule table
        repayments.append({
            "loan_id": loan_id,
            "payment_number": i,
            "payment_date": payment_date,
            "principal_amount": principal_amount,
            "interest_amount": interest_amount,
            "total_payment": monthly_payment,
            "balance": balance
        })

    # Insert all the repayments into the RepaymentSchedule table
    conn.execute(text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :total_payment, :balance)"), repayments)

    # Commit the changes
    conn.commit()

    # Return the repayment schedule
    return repayments
