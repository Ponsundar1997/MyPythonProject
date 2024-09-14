Python
from sqlalchemy import create_engine, text
from config import engine

def transfer(amount, sender, receiver):
    try:
        # Create a connection to the database
        conn = engine.connect()

        # DDL commands (optional)
        # Example: Create a table if it doesn't exist
        # conn.execute(text("CREATE TABLE IF NOT EXISTS accounts (id INTEGER, balance INTEGER)"))

        # Subtract the amount from the sender's account
        result = conn.execute(text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender"), {'amount': amount, 'sender': sender})
        sender_balance = conn.execute(text("SELECT balance FROM accounts WHERE id = :sender"), {'sender': sender}).scalar()

        # Add the amount to the receiver's account
        result = conn.execute(text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver"), {'amount': amount, 'receiver': receiver})
        receiver_balance = conn.execute(text("SELECT balance FROM accounts WHERE id = :receiver"), {'receiver': receiver}).scalar()

        print(f"Sender's new balance: {sender_balance}")
        print(f"Receiver's new balance: {receiver_balance}")

    except Exception as e:
        print(f"Error transferring amount: {str(e)}")

    finally:
        # Commit the transaction
        conn.close()
