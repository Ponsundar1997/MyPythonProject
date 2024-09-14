
from sqlalchemy import text
from sqlalchemy.engine import create_engine
import pandas as pd

engine = create_engine("postgresql://user:password@host:port/dbname")

def calculate_credit_score(p_customer_id):
    conn = engine.connect()

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(SUM(loan_amount), 0), COALESCE(SUM(repayment_amount), 0), COALESCE(SUM(outstanding_balance), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    result = conn.execute(query, customer_id=p_customer_id)
    total_loan_amount, total_repayment, outstanding_loan_balance = result.fetchone()

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESCE(SUM(balance), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    result = conn.execute(query, customer_id=p_customer_id)
    credit_card_balance = result.fetchone()[0]

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    result = conn.execute(query, customer_id=p_customer_id)
    late_payment_count = result.fetchone()[0]

    # Step 4: Basic rule-based calculation of the credit score
    v_credit_score = 0.0
    if total_loan_amount > 0:
        v_credit_score += (total_repayment / total_loan_amount) * 400
    else:
        v_credit_score += 400

    if credit_card_balance > 0:
        v_credit_score += ((1 - (credit_card_balance / 10000)) * 300)
    else:
        v_credit_score += 300

    v_credit_score -= (late_payment_count * 50)

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Step 5: Update the customer’s credit score in the database
    query = text("""
        UPDATE customers
        SET credit_score = :v_credit_score
        WHERE customers.id = :customer_id
    """)
    conn.execute(query, v_credit_score=v_credit_score, customer_id=p_customer_id)

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :v_credit_score, NOW())
        """)
        conn.execute(query, customer_id=p_customer_id, v_credit_score=v_credit_score)

    conn.commit()
    conn.close()
