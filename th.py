from flask import Flask
app=Flask(__name__)
import time
import threading as T


def generate():
    time.sleep(30)
    return "timetable"


class Lock:
    ulock = T.Lock()
    def lock(f):
        def wrap(*args,**kwargs):
            if  Lock.ulock.locked():
                return str({
                    "status": "fail",
                })
            with Lock.ulock:
                return f(*args,**kwargs)
        return wrap
                

@app.route('/')
@Lock.lock
def index():
    return str(generate())

if __name__ == '__main__':
    app.run(debug=True)