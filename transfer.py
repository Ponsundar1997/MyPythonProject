
from sqlalchemy import text
from config import engine

def transfer_amount(p_sender, p_receiver, p_amount):
    """
    Transfer amount from sender's account to receiver's account.
    
    Parameters:
    p_sender (int): Sender's account ID.
    p_receiver (int): Receiver's account ID.
    p_amount (float): Amount to be transferred.
    """
    
    # Create a SQL text object
    query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
    
    # Execute the UPDATE query to subtract the amount from the sender's account
    engine.execute(query, {'amount': p_amount, 'sender': p_sender})
    
    # Create another SQL text object for adding the amount to the receiver's account
    query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
    
    # Execute the UPDATE query to add the amount to the receiver's account
    engine.execute(query, {'amount': p_amount, 'receiver': p_receiver})

# Usage example:
transfer_amount(1, 2, 100.0)  # Transfer 100.0 from account 1 to account 2
