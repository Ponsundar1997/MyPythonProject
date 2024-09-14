
from config import engine
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
import pandas as pd

def transfer_funds(sender: int, receiver: int, amount: float) -> None:
    engine.execute(text("begin"))
    
    with engine.connect() as connection:
        connection.execute(text("update accounts set balance = balance - :amount where id = :sender").bindparams(sender=sender, amount=amount))
        connection.execute(text("update accounts set balance = balance + :amount where id = :receiver").bindparams(receiver=receiver, amount=amount))
    
    engine.execute(text("commit"))

# Usage:
transfer_funds(1, 2, 100.0)
