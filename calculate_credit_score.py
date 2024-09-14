
from sqlalchemy import create_engine, text
from pandas import Series
from config import engine

def update_customer_credit_score(p_customer_id):
    with engine.connect() as conn:
        # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
        total_loan_amount_query = text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) AS total_loan_amount,
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0) AS total_repayment,
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0) AS outstanding_balance
            FROM loans
            WHERE loans.customer_id = :p_customer_id
        """)
        total_loan_amount_results = conn.execute(total_loan_amount_query, p_customer_id=p_customer_id)
        total_loan_amount, total_repayment, outstanding_balance = total_loan_amount_results.fetchone()

        # Step 2: Get the current credit card balance
        credit_card_balance_query = text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0) AS credit_card_balance
            FROM credit_cards
            WHERE credit_cards.customer_id = :p_customer_id
        """)
        credit_card_balance_results = conn.execute(credit_card_balance_query, p_customer_id=p_customer_id)
        credit_card_balance = credit_card_balance_results.fetchone()[0]

        # Step 3: Count the number of late payments
        late_pay_count_query = text("""
            SELECT COUNT(*) AS late_pay_count
            FROM payments
            WHERE payments.customer_id = :p_customer_id AND status = 'Late'
        """)
        late_pay_count_results = conn.execute(late_pay_count_query, p_customer_id=p_customer_id)
        late_pay_count = late_pay_count_results.fetchone()[0]

        # Step 4: Basic rule-based calculation of the credit score
        v_credit_score = 0
        if total_loan_amount > 0:
            v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)
        else:
            v_credit_score += 400

        if credit_card_balance > 0:
            v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)
        else:
            v_credit_score += 300

        v_credit_score -= late_pay_count * 50

        # Ensure the score stays within reasonable bounds
        if v_credit_score < 300:
            v_credit_score = 300
        elif v_credit_score > 850:
            v_credit_score = 850

        # Step 5: Update the customer’s credit score in the database
        update_query = text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """)
        conn.execute(update_query, p_customer_id=p_customer_id, v_credit_score=v_credit_score)

        # Optionally, log the result or raise an alert for very low scores
        if v_credit_score < 500:
            insert_query = text("""
                INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
                VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
            """)
            conn.execute(insert_query, p_customer_id=p_customer_id, v_credit_score=v_credit_score)

        conn.commit()

    return v_credit_score
