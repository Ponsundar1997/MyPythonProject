
from config import engine
from sqlalchemy import text
import pandas as pd

def transfer_amount(sender_id, receiver_id, amount):
    # Subtract amount from sender's account
    update_sender = text("""
        update accounts 
        set balance = balance - :amount 
        where id = :sender_id
    """)
    engine.execute(update_sender, sender_id=sender_id, amount=amount)

    # Add amount to receiver's account
    update_receiver = text("""
        update accounts 
        set balance = balance + :amount 
        where id = :receiver_id
    """)
    engine.execute(update_receiver, receiver_id=receiver_id, amount=amount)

    # Commit changes
    engine.commit()

accounts_df = pd.read_sql_table('accounts', engine)
# Perform additional operations on the DataFrame
