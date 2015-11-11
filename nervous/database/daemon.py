import datetime
import time

import api.update as api_update

def update_all():
    api_update.update_all()

def daemon():
    while True:
        print "update_all"
        update_all()
        now = datetime.datetime.now()
        delta_day = datetime.timedelta(days = 1)
        tomorrow = now + delta_day
        target_time = tomorrow.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        delta = target_time - now
        secs = delta.total_seconds()
        print "next update time: %s (%s seconds later)" % (
            target_time,
            secs
        )
        time.sleep(secs)
