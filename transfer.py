
from sqlalchemy import create_engine, text
from config import engine
import pandas as pd

def your_function(param1, param2):
    conn = engine.connect()
    result = conn.execute(text("""
        BEGIN;
        -- some DDL commands here
        CREATE TEMP TABLE temp_table AS
        SELECT * FROM your_table WHERE your_column = :param1;
        CREATE INDEX idx_temp_table ON temp_table(your_index_column);
        COMMIT;
    """), {'param1': param1})
    
    result = conn.execute(text("""
        SELECT * FROM temp_table
        WHERE another_column = :param2
        ORDER BY some_column;
    """), {'param2': param2})
    
    df = pd.DataFrame(result.fetchall(), columns=[x.key for x in result.keys()])
    return df
