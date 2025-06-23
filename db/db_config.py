import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

from db.queries import Queries

load_dotenv()

class DB:
    def __init__(self):
        self.__connection = None
        self.__queries = None
        self.__db_name = os.getenv("DB_NAME")

        try:
            # Step 1: Connect to MySQL server without specifying a database
            temp_conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                use_pure=True
            )

            if temp_conn.is_connected():
                cursor = temp_conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.__db_name}")
                print(f"Database '{self.__db_name}' ensured.")
                cursor.close()
                temp_conn.close()

            # Step 2: Connect to the actual database
            self.__connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=self.__db_name,
                use_pure=True
            )

            if self.__connection.is_connected():
                print(f"Connected to MySQL database '{self.__db_name}'")

                # Step 3: Initialize Queries to create tables
                self.__queries = Queries(self.__connection)

        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def get_connection(self):
        return self.__connection

    def close(self):
        if self.__queries:
            del self.__queries
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()
            print("Connection closed")

    def __del__(self):
        self.close()