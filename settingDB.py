import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

class setDB:
    def __init__(self):
        load_dotenv()
        #mysql con
        db=os.environ.get("FULLSOURCE")
        self.db_connection=create_engine(db)
        self.conn=self.db_connection.connect()
    
    def close(self):
        self.conn.close()