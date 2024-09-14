
from sqlalchemy import create_engine, text
from config import engine
import pandas as pd

def calculate_repayment_schedule(loan_id):
    # Create a connection to the database
    conn = engine.connect()
    
    # Execute a query to get the loan details
    result = conn.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), loan_id=loan_id)
    loan_details = result.fetchone()
    loan_amount, interest_rate, loan_term, start_date = loan_details
    
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12
    
    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))
    
    # Initialize balance to the loan amount
    balance = loan_amount
    
    # Initialize payment date to the start date of the loan
    payment_date = start_date
    
    # Initialize payment number to 1
    payment_number = 1
    
    # Create a list to store the repayment schedule
    repayment_schedule = []
    
    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate
        
        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount
        
        # Deduct principal from balance
        balance = balance - principal_amount
        
        # Insert repayment details into the RepaymentSchedule table
        repayment_schedule.append({
            'loan_id': loan_id,
            'payment_number': payment_number,
            'payment_date': payment_date,
            'principal_amount': principal_amount,
            'interest_amount': interest_amount,
            'total_payment': monthly_payment,
            'balance': balance
        })
        
        # Move to the next month
        payment_date = payment_date + pd.DateOffset(months=1)
        payment_number += 1
    
    # Close the connection
    conn.close()
    
    # Return the repayment schedule
    return repayment_schedule
