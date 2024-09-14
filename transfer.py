
from config import engine
import pandas as pd

def execute_transaction(sender, receiver, amount):
    # Subtract the amount from the sender's account
    update_sender = """
        UPDATE accounts
        SET balance = balance - {amount}
        WHERE id = {sender};
    """.format(sender=sender, amount=amount)
    result = engine.execute(text(update_sender))  # Execute the query
    engine.commit()  # Commit the transaction

    # Add the amount to the receiver's account
    update_receiver = """
        UPDATE accounts
        SET balance = balance + {amount}
        WHERE id = {receiver};
    """.format(receiver=receiver, amount=amount)
    result = engine.execute(text(update_receiver))  # Execute the query
    engine.commit()  # Commit the transaction
