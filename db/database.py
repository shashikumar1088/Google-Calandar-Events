import os
import inspect
import sqlite3 as sql3
from error import Error

class Database(Error):
    dbName = 'GC'
    con = None
    cur = None
    def _connect(self):
        try:
            db = os.path.join(os.path.dirname(__file__), self.dbName + '.db')
            self.con = sql3.connect(db, check_same_thread=False)
            self.cur = self.con.cursor()
        except sql3.Error as e:
            raise Exception(f"Error creating/connecting to database: {e}")
       
    def __del__(self):
        if self.con:
            self.con.close()

    def executeQuery(self, query, params = None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
                
            self.con.commit()
            return True
        except sql3.Error as e:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            raise Exception(f"Error in query execution: {e} while calling from {calframe[1][3]}")

    def executeMany(self, query, params):
        try:
            self.cur.executemany(query, params)
            self.con.commit()
            return True
        except sql3.Error as e:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)            
            raise Exception(f"Error in query execution: {e} while calling from {calframe[1][3]}")
        
    def dropTable(self, tableName) -> bool:
        return self.executeQuery(f'DROP TABLE IF EXISTS {tableName};')
    
    def trucateTable(self, tableName) -> bool:
        return self.executeQuery(f'DELETE FROM {tableName};')

    def fetchAllRows(self, query, params = None) -> list:
        try:
            self.cur.execute(query)                
            self.con.commit()
            return self.cur.fetchall()
        except sql3.Error as e:
            self.error = f"Error fetching rows: {e}"
            print(self.error)
            return []

    def printTableData(self, tableName):
        # Fetch and print the table data
        table_data = self.fetchAllRows(f"SELECT * FROM {tableName};")
        print("Table Data:")
        print(table_data)

    def printTableStructureAndData(self):
        # Get a list of all tables in the database
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()

        # Loop through the tables and print their structure and data
        for table in tables:
            tableName = table[0]
            print(f"Table Name: {tableName}")

            # Get the table structure
            self.cur.execute(f"PRAGMA table_info({tableName});")
            table_structure = self.cur.fetchall()

            # Print the table structure
            print("Table Structure:")
            for column in table_structure:
                column_name = column[1]
                data_type = column[2]
                is_nullable = "YES" if column[3] == 1 else "NO"
                print(f"  Column Name: {column_name}")
                print(f"  Data Type: {data_type}")
                print(f"  Nullable: {is_nullable}")
                print()

            self.printTableData(tableName)
