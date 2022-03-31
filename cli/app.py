import sys
from __future__ import annotations

from db import DBHelper
from flask import Flask, jsonify, request

sys.path.append("..")

from timetable_generator.backtrack import generate as timetable_generator

app = Flask(__name__)

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

db_helper = DBHelper()


@app.route("/generate")
def generate():
    timetable_rows = []
    final_timetable = timetable_generator()
    for class_, timetable in final_timetable.items():
        for day_index, row in enumerate(timetable):
            if day_index == 5:
                print(day_index, class_)
            timetable_rows.append(
                (*class_, DAYS[day_index], *[period.subject.name for period in row])
            )
    db_helper.generateDB(timetable_rows)
    return jsonify({"status": "success", "message": "generated"})


@app.route("/getTimeTable")
def table():
    args = request.args
    std = args.get("std")
    section = args.get("section")
    subject = args.get("subject")

    # sub the particular subject with the respective class
    if std and subject:
        data = {}
        result = db_helper.getTimeTableStd(std)
        converted = convertToTeacherTimeTable(result, subject)
        data["message"] = converted
        return jsonify(data)

    if std and section:
        data = {}
        data["message"] = db_helper.getTimeTable(std, section)
        return jsonify(data)

    if std:
        data = {}
        data["message"] = db_helper.getTimeTableStd(std)
        return jsonify(data)

    return "INVLID!!!!"


if __name__ == "__main__":
    app.run(debug=True)
