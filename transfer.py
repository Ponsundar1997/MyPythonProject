Python
from config import engine
from sqlalchemy import create_engine, text
import pandas as pd

# create a connection
if engine.url.drivername == 'postgresql':
    conn = create_engine('postgresql://' + engine.url.username + ':' + engine.url.password + '@' + engine.url.host + ':' + str(engine.url.port) + '/' + engine.url.database)
else:
    conn = engine

# sender and receiver IDs
sender = 1
receiver = 2
amount = 100

# subtracting the amount from the sender's account 
update_sender_sql = """
update accounts 
set balance = balance - :amount 
where id = :sender;
"""
result_sender = conn.execute(text(update_sender_sql), sender=sender, amount=amount)

# adding the amount to the receiver's account
update_receiver_sql = """
update accounts 
set balance = balance + :amount 
where id = :receiver;
"""
result_receiver = conn.execute(text(update_receiver_sql), receiver=receiver, amount=amount)

# commit the changes
conn.execute("COMMIT;")
