from collections import defaultdict
from db import getTimeTable, getTimeTableStd,generateDB
from flask import Flask,request,jsonify

import sys
sys.path.append("..")

from timetable_generator.backtrack import generate as timetable_generator
app=Flask(__name__)

DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday"]

@app.route('/generate')
def generate():
    timetable_rows =[]
    final_timetable = timetable_generator()
    for class_,timetable in final_timetable.items():
        for day_index,row in enumerate(timetable):
            if day_index==5:
                print(day_index,class_)
            timetable_rows.append((*class_,DAYS[day_index],*[period.subject.name for period in row]))
    generateDB(timetable_rows)
    return jsonify({'status':'success','message':'generated'})

@app.route('/getTimeTable')
def table():
    args = request.args
    std = args.get('std')
    section = args.get('section')
    subject=args.get('subject')

    #sub the particular subject with the respective class
    if std and subject:
        map={}
        result=getTimeTableStd(std)
        converted=convertToTeacherTimeTable(result,subject)
        map["message"]=converted
        return jsonify(map)

    if std and section:
        map={}
        map["message"]=getTimeTable(std,section)
        return jsonify(map)

    if std:
        map={}
        map["message"]=getTimeTableStd(std)
        return jsonify(map)
        
    return "INVLID!!!!"

def convertToTeacherTimeTable(timetable, subject):
    columns = ["p_1", "p_2", "p_3", "p_4", "p_5", "p_6"]
    final = defaultdict(lambda: ["-"] * 6)
    for row in timetable:
        for col in columns:
            if row[col] == subject:
                final[row["day"]][columns.index(col)] = f"{row['std']}-{row['section']}"
    print(list(final.values()))
    return list(final.values())

if __name__ == '__main__':
    app.run(debug=True)