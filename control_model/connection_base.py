from dotenv import load_dotenv
import os
import psycopg2

from psycopg2 import OperationalError

class ETDLP_Control_Model_Base():
    
    def create_connection():
        load_dotenv()
        connection = None
        try:
            connection = psycopg2.connect(
                database=os.getenv("db_name"),
                user=os.getenv("db_user"),
                password=os.getenv("db_password"),
                host=os.getenv("db_host"),
                port=os.getenv("db_port")
                )
            
            print("Connection to PostgreSQL DB successful")
            
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            
        return connection