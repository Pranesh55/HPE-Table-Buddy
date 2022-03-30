from collections import defaultdict
from db import getTimeTable, getTimeTableStd
from flask import Flask,request,jsonify

app=Flask(__name__)


@app.route('/generate')
def genrate():
    #call generate function
    #put the result into db
    return jsonify({'status':'success','message':'generated'})

@app.route('/getTimeTable')
def home():
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