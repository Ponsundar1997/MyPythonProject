Python
from sqlalchemy import text, create_engine
from config import engine

def transfer_funds(sender_id, receiver_id, p_amount):
    try:
        # Execute DDL command if needed
        engine.execute(text("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance INTEGER)"))

        # Subtract the amount from the sender's account
        engine.execute(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"),
                       p_sender=sender_id, p_amount=p_amount)
        
        # Add the amount to the receiver's account
        engine.execute(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"),
                       p_receiver=receiver_id, p_amount=p_amount)
        
        # Commit the operation
        engine.connect().commit()
    except Exception as e:
        # Handle any exceptions
        print(f"Error: {e}")
        engine.connect().rollback()
