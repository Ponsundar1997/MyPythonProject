
from config import engine
import pandas as pd
from sqlalchemy import text

def calculate_repayment_schedule(loan_id):
    conn = engine.connect()
    
    # Execute the DDL commands if needed
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS repayment_schedule (
            loan_id INT,
            payment_number INT,
            payment_date DATE,
            principal_amount DECIMAL(15, 2),
            interest_amount DECIMAL(15, 2),
            total_payment DECIMAL(15, 2),
            balance DECIMAL(15, 2)
        );
    """))
    
    # Get loan details
    loan_data = pd.read_sql_query(f"""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = {loan_id};
    """, conn)
    
    loan_amount = loan_data['loanamount'].values[0]
    interest_rate = loan_data['interestrate'].values[0]
    loan_term = loan_data['loanterm'].values[0]
    start_date = loan_data['startdate'].values[0]
    
    # Convert annual interest rate to monthly interest rate (divide by 12)
    monthly_interest_rate = interest_rate / 100 / 12
    
    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow((1 + monthly_interest_rate), -loan_term))
    
    # Initialize balance to the loan amount
    balance = loan_amount
    
    # Initialize payment_date to the start date of the loan
    payment_date = start_date
    
    # Loop through each month and calculate the repayment schedule
    for payment_number in range(1, loan_term + 1):
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate
        
        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount
        
        # Deduct principal from balance
        balance -= principal_amount
        
        # Insert repayment details into the RepaymentSchedule table
        conn.execute(text("""
            INSERT INTO repayment_schedule (loan_id, payment_number, payment_date, principal_amount, interest_amount, total_payment, balance)
            VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance);
        """), {
            'loan_id': loan_id,
            'payment_number': payment_number,
            'payment_date': payment_date,
            'principal_amount': principal_amount,
            'interest_amount': interest_amount,
            'monthly_payment': monthly_payment,
            'balance': balance
        })
        
        # Move to the next month
        payment_date += pd.Timedelta(days=30)  # Assuming a month has 30 days
        payment_number += 1
    
    conn.close()
