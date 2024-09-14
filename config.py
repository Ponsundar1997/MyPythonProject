from sqlalchemy.engine import URL
 
conn_url = URL.create(
            drivername="postgresql",  # Change this to your specific database driver
            username="postgres",
            password="password",  # Password with special characters
            host="localhost",
            port=str(5432),  # Change this to your specific port
            database="sample"
        )
engine1 = sqlalchemy.create_engine (conn_url)      
conn = engine1.connect()
