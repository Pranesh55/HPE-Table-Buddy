from db import getTimeTable, getTimeTableStd
from flask import Flask,request

app=Flask(__name__)


@app.route('/generate')
def genrate():
    #call generate function
    #put the result into db
    return {'status':'success','message':'generated'}

@app.route('/getTimeTable')
def home():
    args = request.args
    std = args.get('std')
    section = args.get('section')
    if std and section:
        map={}
        map["message"]=getTimeTable(std,section)
        return map
    if std:
        map={}
        map["message"]=getTimeTableStd(std)
        return map
    return "INVLID!!!!"

if __name__ == '__main__':
 
    app.run()