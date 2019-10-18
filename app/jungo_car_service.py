#!/usr/bin/env python
# encoding=utf-8
import traceback
import os
import sys
from apscheduler.schedulers.background import BlockingScheduler
import datetime
import pytz

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from app.crawler import crawler
from app.notifier import notifier
from app.distinguisher import distinguisher
from app.repository import app_repository
from app.model.division_state_cars import DivisionStateCars

working_interval_sec = 60 * 1


def init_notify():
    notifier.hello_notify()


def start_scheduled_job():
    sched = BlockingScheduler()
    sched.add_job(main, 'interval',
                  seconds=working_interval_sec, id="real_time_1")
    sched.start()


def main():
    print(str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
    try:
        data = crawler.crawler()
        dsc: DivisionStateCars = distinguisher.distinguish(data)
        app_repository.update_leave_and_deleted(dsc)
        notifier.notify(dsc)
        print("루프 끝")
    except:
        print("작업 중 문제가 발생함.")
        traceback.print_exc()
        pass    
    

if __name__ == "__main__":
    print(u"Running jungo-car-app!")
    init_notify()
    print(u"Notifier is successfully working!")
    main()
    start_scheduled_job()

# def test():
#     app_repository    
    
# test()