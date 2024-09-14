
from sqlalchemy import create_engine, text
from sqlalchemy.engine import connect
import pandas as pd
from config import engine

def my_function(date_start, date_end):
    # Create a connection to the database
    conn = engine.connect()

    # Execute the SQL query with parameters
    result = conn.execute(text("""
        SELECT 
            column1, 
            column2, 
            column3 
        FROM 
            my_table 
        WHERE 
            date_column >= :date_start 
        AND 
            date_column <= :date_end
    """), {"date_start": date_start, "date_end": date_end})

    # Fetch all the rows
    rows = result.fetchall()

    # Close the connection
    conn.close()

    # Convert the result to a pandas DataFrame
    df = pd.DataFrame(rows, columns=[i[0] for i in result.keys()])
    return df
