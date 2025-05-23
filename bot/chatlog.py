import os
import datetime
import psycopg2

class Chatlog:

    def __init__(self):
        self.debug = False
        self.service_mode = False
        self.CHATBOT_POSTGRES_PASSWORD = os.getenv("CHATBOT_POSTGRES_PASSWORD")
        self.CHATBOT_POSTGRES_USER = os.getenv("CHATBOT_POSTGRES_USER")
        self.CHATBOT_POSTGRES_DB = os.getenv("CHATBOT_POSTGRES_DB")
    
    def connect(self):
        self.connection = psycopg2.connect(
            database=self.CHATBOT_POSTGRES_DB,
            host="postgres",
            user=self.CHATBOT_POSTGRES_USER,
            password=self.CHATBOT_POSTGRES_PASSWORD,
            port=5432
        )
        return self.connection
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def insert_row(
            self,
            log_channel,
            log_message,
            log_user,
            log_timestamp
        ):
        cursor = self.connect().cursor()
        
        query = \
            """ INSERT INTO chatlog 
            (log_channel,
            log_message,
            log_user,
            log_timestamp) 
            VALUES 
            (%s,%s,%s,%s)"""
        
        record_to_insert = (
            log_channel,
            log_message,
            log_user,
            log_timestamp
        )

        cursor.execute(query, record_to_insert)

        self.connection.commit()
        count = cursor.rowcount
        
        if self.debug:
            print(count, "Record inserted successfully into mobile table")
        
        self.disconnect()

    def get_all_log_entries(self):
        cursor = self.connect().cursor()
        cursor.execute("SELECT log_channel,log_message,log_user,log_timestamp FROM chatlog")
        rows = cursor.fetchall()
        if self.debug:
            for table in rows:
                print(table)
        self.disconnect()

    def _create_table(self):
        if not self.service_mode:
            return

        sql = """
            CREATE TABLE chatlog (
                log_id bigserial primary key,
                log_channel varchar(255),
                log_message text,
                log_user VARCHAR(255),
                log_timestamp TIMESTAMPTZ
            );
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def _drop_table(self):
        if not self.service_mode:
            return

        sql = """   
            DROP TABLE IF EXISTS chatlog;
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()