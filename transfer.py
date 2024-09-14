Python
from sqlalchemy.sql import text
from config import engine
import pandas as pd

def transfer_funds(sender, receiver, amount):
    # Subtracting the amount from the sender's account
    query = text("""
        UPDATE accounts 
        SET balance = balance - :amount 
        WHERE id = :sender
    """)
    engine.execute(query, {'sender': sender, 'amount': amount})
    
    # Adding the amount to the receiver's account
    query = text("""
        UPDATE accounts 
        SET balance = balance + :amount 
        WHERE id = :receiver
    """)
    engine.execute(query, {'receiver': receiver, 'amount': amount})
    
    # Commit changes
    engine.connect().commit()
Python
from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///example.db')  # Create an engine
metadata = MetaData()

# Create the table
metadata.create_all(engine)

# Drop the table (DDL)
metadata.drop_all(engine)
