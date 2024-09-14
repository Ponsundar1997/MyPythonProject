
from config import engine
import pandas as pd
from sqlalchemy import text

def transfer_between_accounts(sender, receiver, amount):
    # Subtract the amount from the sender's account
    update_query = text("""
        update accounts 
        set balance = balance - :amount 
        where id = :sender;
    """)
    engine.execute(update_query, {"sender": sender, "amount": amount})

    # Add the amount to the receiver's account
    update_query = text("""
        update accounts 
        set balance = balance + :amount 
        where id = :receiver;
    """)
    engine.execute(update_query, {"receiver": receiver, "amount": amount})

    # Commit the transaction
    engine.execute("commit")

engine.execute(text("CREATE TABLE IF NOT EXISTS accounts (id SERIAL PRIMARY KEY, balance INTEGER)"))
