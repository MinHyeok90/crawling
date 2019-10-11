#!/usr/bin/env python
# encoding=utf-8
import os
import sys
from apscheduler.schedulers.background import BlockingScheduler
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from app.crawler import crawling
from app.notifier import notifier
from app.distinguisher import distinguisher
from app.repository import app_repository

working_interval_sec = 600
health_check_sec = 1


def repeat_job():
    sched = BlockingScheduler()
    sched.add_job(main, 'interval', seconds=working_interval_sec, id="test_interval_1")
    sched.start()


def main():
    print(u"running jungo-car-app! (" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")")
    data = crawling.crawling()
    distinguished_cars = distinguisher.distinguish(data)
    app_repository.update_leave_and_deleted(distinguished_cars)
    notifier.notify(distinguished_cars)


main()
repeat_job()
