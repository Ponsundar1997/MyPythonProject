
from SQLAlchemy import text
from config import engine
import pandas as pd

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    try:
        # Subtract the amount from the sender's account
        conn.execute(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), p_amount=p_amount, p_sender=p_sender)
        
        # Add the amount to the receiver's account
        conn.execute(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), p_amount=p_amount, p_receiver=p_receiver)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        conn.close()
