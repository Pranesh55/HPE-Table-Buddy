from inspect import classify_class_attrs
import sqlite3
from typing import Tuple

def getConn():
    connection = sqlite3.connect('database.db')
    return connection

def getTimeTable(std,section):
    cur=getConn().cursor()
    tab=cur.execute("select * from TimeTable where std=? and section=?",(std,section))
    resultTimeTable=[]
    for t in tab:
        map={}
        map["std"]=t[0]
        map["section"]=t[1]
        map["day"]=t[2]
        map["p_1"]=t[3]
        map["p_2"]=t[4]
        map["p_3"]=t[5]
        map["p_4"]=t[6]
        map["p_5"]=t[7]
        map["p_6"]=t[8]
        resultTimeTable.append(map)
    return resultTimeTable

def getTimeTableStd(std):
    connection=getConn()
    cur=connection.cursor()
    tab=cur.execute("select * from TimeTable where std=?",(std,))
    resultTimeTable=[]
    for t in tab:
        map={}
        map["std"]=t[0]
        map["section"]=t[1]
        map["day"]=t[2]
        map["p_1"]=t[3]
        map["p_2"]=t[4]
        map["p_3"]=t[5]
        map["p_4"]=t[6]
        map["p_5"]=t[7]
        map["p_6"]=t[8]
        resultTimeTable.append(map)
    return resultTimeTable
    

def generate():
    truncateTable()
    return

def truncateTable():
    connection=getConn()
    cur=connection.cursor()
    cur.execute("delete from TimeTable")
    connection.commit()
    return 

def insertInTo(list):
    connection=getConn()
    cur=connection.cursor()
    cur.execute("insert into TimeTable values(?,?,?,?,?,?,?,?,?)",tuple(list))
    connection.commit()
    print(list)
    return


# con=getConn()
# cur=con.cursor()
# cur.execute("create table TimeTable(std varchar,section varchar,day varchar,p_1 varchar,p_2 varchar,p_3 varchar,p_4 varchar,p_5 varchar,p_6 varchar);")

# truncateTable()
#insertInTo(['I','A','Monday',"Maths","English","SST","Music","Tam","Science"])
# insertInTo(['I','B','Tuesday',"Eng","Maths","SST","Music","Tam","Science"])
# insertInTo(['I','B','Wednesday',"Eng","Maths","SST","Music","Tam","Science"])
# insertInTo(['I','B','Thursday',"Eng","Maths","SST","Music","Tam","Science"])
# insertInTo(['I','B','Friday',"Eng","Maths","SST","Music","Tam","Science"])

#print(getTimeTableStd('I'))
#truncateTable()
#print(getTimeTable('I','A'))