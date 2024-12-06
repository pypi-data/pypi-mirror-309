# my_database_lib/database.py

import pyodbc
import pandas as pd


class Database:
    def __init__(self, server, database, user=None, password=None, driver='ODBC Driver 17 for SQL Server'):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.driver = driver
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            # Ha nincs megadva felhasználónév és jelszó, akkor Windows hitelesítést használunk
            if self.user and self.password:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password}'
            else:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'

            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("INFO: Connected to SQL Server")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Unable to connect to SQL Server: {e}\033[0m")

    def insert_row(self, row_data, table):
        try:
            # Példa SQL insert query
            columns = ', '.join(row_data.keys())
            placeholders = ', '.join(['?' for _ in row_data])
            sql_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql_query, tuple(row_data.values()))
            self.conn.commit()
            print("INFO: Row inserted successfully")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to insert row: {e}\033[0m")

    def update_row(self, keys, updates, table):
        try:
            # Példa SQL update query
            set_clause = ', '.join([f"{k} = ?" for k in updates])
            where_clause = ' AND '.join([f"{k} = ?" for k in keys])
            sql_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(sql_query, tuple(updates.values()) + tuple(keys.values()))
            self.conn.commit()
            print("INFO: Row updated successfully")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to update row: {e}\033[0m")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print("INFO: Query executed successfully")
            return results
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to execute query: {e}\033[0m")
            return None

    def get_table(self, table):
        try:
            query = f"SELECT * FROM {table}"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]  # Oszlopnevek kinyerése
            rows = self.cursor.fetchall()
            table_df = pd.DataFrame.from_records(rows, columns=columns)

            # Tábla adatainak levágása
            trimmed_table = self.trim_table_data(table_df)
            print("INFO: Table fetched successfully")
            return trimmed_table
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to fetch table: {e}\033[0m")
            return None

    def trim_table_data(self, table):
        # Ez a metódus eltávolítja a fölösleges szóközöket a cellák értékeiből
        for col in table.columns:
            if table[col].dtype == object:  # Ha az oszlop értékei karakterláncok
                table[col] = table[col].str.strip()
        return table

    def close(self):
        if self.conn:
            self.conn.close()
            print("INFO: Connection to SQL Server closed")
