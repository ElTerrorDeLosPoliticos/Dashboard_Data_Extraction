import psycopg2

class Close_Control_ModeL_Connection():
    
    @staticmethod
    def close_connection(self):
        try:    
            connection = self.connection
            cursor = connection.cursor()
            if connection is not None:
                cursor.close()
                connection.close()
                print("Connection to PostgreSQL DB was closed successful")

        except (Exception, psycopg2.OperationalError) as e:
            print(f"The error '{e}' occurred")
            connection.rollback()
            raise
        
        return True