import sqlite3
from inspect import classify_class_attrs
from typing import Tuple
import roman

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBHelper(metaclass=Singleton):
    def __init__(self) -> None:
        self.conn = sqlite3.connect("database.db",check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS TimeTable(
                std varchar,
                section varchar,
                day varchar,
                p_1 varchar,
                p_2 varchar,
                p_3 varchar,
                p_4 varchar,
                p_5 varchar,
                p_6 varchar)
        """
        )
        self.conn.commit()

    def getTimeTable(self, std, section):
        cur = self.conn.cursor()
        tab = cur.execute("select * from TimeTable where std=? and section=?", (std, section))
        resultTimeTable = []
        for t in tab:
            data = {}
            data["std"] = t[0]
            data["section"] = t[1]
            data["day"] = t[2]
            data["p_1"] = t[3]
            data["p_2"] = t[4]
            data["p_3"] = t[5]
            data["p_4"] = t[6]
            data["p_5"] = t[7]
            data["p_6"] = t[8]
            resultTimeTable.append(data)
        return resultTimeTable

    def getTimeTableStd(self, std):
        cur = self.conn.cursor()
        tab = cur.execute("select * from TimeTable where std=?", (std,))
        resultTimeTable = []
        for t in tab:
            print(t)
            data = {}
            data["std"] = t[0]
            data["section"] = t[1]
            data["day"] = t[2]
            data["p_1"] = t[3]
            data["p_2"] = t[4]
            data["p_3"] = t[5]
            data["p_4"] = t[6]
            data["p_5"] = t[7]
            data["p_6"] = t[8]
            resultTimeTable.append(data)
        return resultTimeTable

    def generateDB(self, timetable_rows: list):
        self.truncateTable()
        for row in timetable_rows:
            self.insertInto(row)

        return

    def truncateTable(self):
        cur = self.cursor
        cur.execute("delete from TimeTable")
        self.conn.commit()
        return

    def insertInto(self, timetable_row: tuple):
        cur = self.cursor
        cur.execute("insert into TimeTable values(?,?,?,?,?,?,?,?,?)", timetable_row)
        self.conn.commit()
        return


# con=getConn()
# cur=con.cursor()
# cur.execute("create table TimeTable(std varchar,section varchar,day varchar,p_1 varchar,p_2 varchar,p_3 varchar,p_4 varchar,p_5 varchar,p_6 varchar);")

# truncateTable()
# insertInTo(['I','A','Monday',"Maths","English","SST","Music","Tam","Science"])
# insertInTo(['I','B','Tuesday',"Eng","Maths","SST","Music","Tam","Science"])
# insertInTo(['I','B','Wednesday',"Eng","Maths","SST","Music","Tam","Science"])
# insertInTo(['I','B','Thursday',"Eng","Maths","SST","Music","Tam","Science"])
# insertInTo(['I','B','Friday',"Eng","Maths","SST","Music","Tam","Science"])

# print(getTimeTableStd('I'))
# truncateTable()
# print(getTimeTable('I','A'))
