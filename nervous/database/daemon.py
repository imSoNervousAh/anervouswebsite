import datetime
import time

import backend


def update_all():
    backend.update_all()



def daemon():
    while True:
        update_all()
        now = datetime.datetime.now()
        delta_day = datetime.timedelta(days=1)
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
