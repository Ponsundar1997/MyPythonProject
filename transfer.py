
from config import engine
from sqlalchemy import text
import pandas as pd

def transfer Funds(sender_id, receiver_id, amount):
    # Create a connection to the database
    conn = engine.connect()

    # Subtract the amount from the sender's account
    query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
    result = conn.execute(query, {'sender': sender_id, 'amount': amount})
    sender_balance = conn.execute(text("SELECT balance FROM accounts WHERE id = :sender"), {'sender': sender_id}).scalar()

    # Add the amount to the receiver's account
    query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
    result = conn.execute(query, {'receiver': receiver_id, 'amount': amount})
    receiver_balance = conn.execute(text("SELECT balance FROM accounts WHERE id = :receiver"), {'receiver': receiver_id}).scalar()

    # Commit the changes
    conn.commit()
    conn.close()

    # Print the final balances
    print(f"Sender's new balance: {sender_balance}")
    print(f"Receiver's new balance: {receiver_balance}")
