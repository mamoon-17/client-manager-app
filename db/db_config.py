import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

class DB:
    def __init__(self):
        self.__connection = None

        try:
            self.__connection = mysql.connector.connect(
                host= os.getenv("DB_HOST"),
                user= os.getenv("DB_USER"),
                password= os.getenv("DB_PASS"),
                database= os.getenv("DB_NAME"),
                use_pure=True
            )
            if self.__connection.is_connected():
                print("Connected to MySQL DB")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def get_connection(self):
        return self.__connection

    def close(self):
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()
            print("Connection closed")

    def __del__(self):
        self.close()