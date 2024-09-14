
from sqlalchemy import create_engine, text
import pandas as pd

# Load database configuration from config.py
from config import engine

def calculate_repayment_schedule(loan_id):
    # Create a connection to the database
    conn = engine.connect()

    try:
        # Execute the stored procedure query
        loan_amount = None
        interest_rate = None
        loan_term = None
        start_date = None
        with conn.begin():
            result = conn.execute(text("""
                SELECT loanamount, interestrate, loanterm, startdate
                FROM loans
                WHERE loanid = :loan_id;
            """), loan_id=loan_id)

            loan_amount, interest_rate, loan_term, start_date = result.fetchone()

            # Convert annual interest rate to monthly interest rate (divide by 12)
            monthly_interest_rate = interest_rate / 100 / 12

            # Calculate fixed monthly payment using the amortization formula
            monthly_payment = (loan_amount * monthly_interest_rate) / \
                               (1 - pow(1 + monthly_interest_rate, -loan_term))

            # Initialize balance to the loan amount
            balance = loan_amount

            # Initialize payment_date to the start date of the loan
            payment_date = start_date

            # Initialize payment_number to 1
            payment_number = 1

            # Initialize a list to store the repayment schedule
            repayment_schedule = []

            while payment_number <= loan_term:
                # Calculate interest for the current month
                interest_amount = balance * monthly_interest_rate

                # Calculate principal for the current month
                principal_amount = monthly_payment - interest_amount

                # Deduct principal from balance
                balance = balance - principal_amount

                # Append the repayment details to the repayment schedule
                repayment_schedule.append({
                    'payment_date': payment_date,
                    'principal_amount': principal_amount,
                    'interest_amount': interest_amount,
                    'total_payment': monthly_payment,
                    'balance': balance
                })

                # Move to the next month
                payment_date = payment_date + pd.DateOffset(months=1)
                payment_number += 1

            # Insert repayment schedule into the RepaymentSchedule table
            conn.execute(text("""
                INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
                VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance);
            """), loan_id=loan_id, payment_number=payment_number, payment_date=start_date, principal_amount=0, interest_amount=0, monthly_payment=0, balance=loan_amount)

            # Return the repayment schedule
            return dict(repayment_schedule)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        conn.close()
