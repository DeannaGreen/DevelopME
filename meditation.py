from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask import time

meditation = Blueprint('meditation', __name__)

@meditation.route('/meditation')
def timer():
    while True:
        uin = input(">>")
        try:
            when_to_stop = abs(int(uin))
        expect KeyboardInterrupt:
            break
        expect:
            print("Not a number!")

        while when_to_stop > 0:
            m, s = divmod(when_to_stop, 60)
            h, m = divmod(m, 60)
            time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
            print(time_left + "\r", end=" ")
            time.sleep(1)
            when_to_stop -=1
        print()
    return render_template('meditation.html')
