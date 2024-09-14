Python
from sqlalchemy import text
from sqlalchemy.engine import Engine
from config import engine
import pandas as pd

def transfer_funds(p_sender, p_receiver, p_amount):
    try:
        # DDL commands if needed
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance REAL)"))

        # Execute the SQL query with parameters
        with engine.connect() as conn:
            result = conn.execute(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"),
                                  p_amount=p_amount, p_sender=p_sender)
            result = conn.execute(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"),
                                  p_amount=p_amount, p_receiver=p_receiver)

        # Commit the changes
        conn.commit()

    except Exception as e:
        print(e)

    return
