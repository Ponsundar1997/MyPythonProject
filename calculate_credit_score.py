
from sqlalchemy.sql import text
from config import engine

def calculate_credit_score(customer_id):
    """
    Calculate the credit score for a given customer.

    Parameters:
    customer_id (int): The ID of the customer.

    Returns:
    None
    """

    # Create a connection object
    conn = engine.connect()

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id;
    """)

    result = conn.execute(query, customer_id=customer_id)
    row = result.fetchone()

    if row is not None:
        total_loan_amount, total_repayment, outstanding_loan_balance = row
    else:
        total_loan_amount, total_repayment, outstanding_loan_balance = 0, 0, 0

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id;
    """)

    result = conn.execute(query, customer_id=customer_id)
    row = result.fetchone()

    if row is not None:
        credit_card_balance = row[0]
    else:
        credit_card_balance = 0

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT_payments AS late_payment_count
        FROM (
            SELECT COUNT(*) AS COUNT_payments
            FROM payments
            WHERE payments.customer_id = :customer_id AND status = 'Late'
        ) AS subquery;
    """)

    result = conn.execute(query, customer_id=customer_id)
    row = result.fetchone()

    if row is not None:
        late_pay_count = row[0]
    else:
        late_pay_count = 0

    # Step 4: Basic rule-based calculation of the credit score
    # Factor 1: Repayment rate (higher is better)
    v_credit_score = 0
    if total_loan_amount > 0:
        v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)  # 40% weight for loan repayment
    else:
        v_credit_score += 400  # If no loans, give average score for this factor

    # Factor 2: Credit utilization (lower is better)
    if credit_card_balance > 0:
        v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)  # 30% weight for credit card utilization
    else:
        v_credit_score += 300

    # Factor 3: Late payments (fewer is better)
    v_credit_score -= (late_pay_count * 50)  # Deduct 50 points for each late payment

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Step 5: Update the customer’s credit score in the database
    query = text("""
        UPDATE customers
        SET credit_score = ROUND(:credit_score, 0)
        WHERE customers.id = :customer_id;
    """)

    conn.execute(query, credit_score=v_credit_score, customer_id=customer_id)

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, ROUND(:credit_score, 0), NOW());
        """)

        conn.execute(query, customer_id=customer_id, credit_score=v_credit_score)

    # Commit the transaction
    conn.commit()

    # Close the connection object
    conn.close()
