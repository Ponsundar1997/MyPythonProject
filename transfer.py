
from config import engine
from sqlalchemy import text
import pandas as pd

def transfer_amount(sender, receiver, amount):
    conn = engine.connect()
    try:
        # execute update query
        query = text("""
            UPDATE accounts 
            SET balance = balance - :amount 
            WHERE id = :sender;
        """)
        conn.execute(query, sender=sender, amount=amount)

        # execute another update query
        query = text("""
            UPDATE accounts 
            SET balance = balance + :amount 
            WHERE id = :receiver;
        """)
        conn.execute(query, receiver=receiver, amount=amount)

        # commit the changes
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()
