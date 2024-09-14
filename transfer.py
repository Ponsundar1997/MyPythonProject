
import sqlalchemy as sa
from sqlalchemy import text
import pandas as pd
from config import engine

def transfer_funds(sender, receiver, amount):
    # Create a connection to the database
    conn = engine.connect()

    # Subtract the amount from the sender's account
    sender_update = text("""update accounts 
                            set balance = balance - :amount 
                            where id = :sender""")
    conn.execute(sender_update, {"sender": sender, "amount": amount})

    # Add the amount to the receiver's account
    receiver_update = text("""update accounts 
                             set balance = balance + :amount 
                             where id = :receiver""")
    conn.execute(receiver_update, {"receiver": receiver, "amount": amount})

    # Commit the changes
    conn.commit()

    conn.close()
