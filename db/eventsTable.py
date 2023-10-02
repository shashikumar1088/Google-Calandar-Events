import os
import sys
from datetime import datetime 
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

from database import Database

class EventsTable(Database):
    name = 'events'
    def __init__(self):
        self._connect()
        self.__create()
        
    def __create(self):
        self.executeQuery(f'''
                            CREATE TABLE IF NOT EXISTS {self.name}
                            (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                            start_date DATETIME,
                            end_date DATETIME,
                            summary CHAR(150))
                        ''')
        
    def drop(self):
        return self.dropTable(self.name)
    
    def clear(self):
        return self.trucateTable(self.name)

    def add(self, events):
        return self.executeMany(f'''
                                INSERT INTO {self.name} (start_date, end_date, summary) VALUES(?, ?, ?)
                                ''', events)

    def getAll(self, page = 0, pagesize = 31):
        return self.fetchAllRows(f'''SELECT * FROM {self.name} LIMIT {page}, {pagesize}''')
    
    def getAllAfterDate(self, date, page = 0, pagesize = 31):
        data = self.fetchAllRows(f'''
                                 SELECT * FROM {self.name} 
                                 WHERE 
                                    start_date >= '{date}'
                                 LIMIT {page}, {pagesize}
                                ''')
        columns = self.cur.description 
        return [{columns[index][0]:column for index, column in enumerate(value)} for value in data]
    
    def printData(self):
        self.printTableData(self.name)


if '__main__' == __name__:
    tbl = EventsTable()
    # tbl.drop()
    # tbl.clear()
    # res = [
    #     ('2023-10-06T06:00:00+05:30', '2023-10-06T06:00:00+05:30', 'Test'),
    # ]
    # print(tbl.add(res))
    # tbl.printData()
    print(tbl.getAll())