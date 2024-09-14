
from sqlalchemy import create_engine, text
import pandas as pd

# Load the database connection configuration from config.py
from config import engine

def transfer(amount, sender, receiver):
    try:
        # Subtract the amount from the sender's account
        update_sender = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
        engine.execute(update_sender, {"amount": amount, "sender": sender})

        # Add the amount to the receiver's account
        update_receiver = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
        engine.execute(update_receiver, {"amount": amount, "receiver": receiver})

        # Commit the changes
        engine.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        engine.rollback()

    # Return the final result
    conn = engine.connect()
    get_balance_sender = text("SELECT balance FROM accounts WHERE id = :sender")
    result_sender = conn.execute(get_balance_sender, {"sender": sender}).fetchone()
    
    get_balance_receiver = text("SELECT balance FROM accounts WHERE id = :receiver")
    result_receiver = conn.execute(get_balance_receiver, {"receiver": receiver}).fetchone()

    return result_sender[0], result_receiver[0]
