
from config import engine
import pandas as pd

def procedure(sender_id, receiver_id, amount):
    # Subtracting the amount from the sender's account
    update_sender = """
        UPDATE accounts 
        SET balance = balance - {} 
        WHERE id = {};
    """.format(amount, sender_id)
    
    # Adding the amount to the receiver's account
    update_receiver = """
        UPDATE accounts 
        SET balance = balance + {} 
        WHERE id = {};
    """.format(amount, receiver_id)
    
    try:
        conn = engine.connect()
        conn.execute(update_sender)
        conn.execute(update_receiver)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
