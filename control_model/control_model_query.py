import psycopg2
import streamlit as st

class Control_Model_Query():
    
    @staticmethod
    def  query_db(self, query):
            
        connection = None
        
        try:    
            connection = self.connection
            connection.autocommit = True
            cursor = connection.cursor()
            postgres_insert_query = f"{query}"
            cursor.execute(postgres_insert_query)
            result = cursor.fetchall()
        except (Exception, psycopg2.OperationalError) as e:
            print(f"The error '{e}' occurred")
            connection.rollback()
            raise
        return result