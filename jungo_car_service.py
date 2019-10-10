#!/usr/bin/env python
# encoding=utf-8

import crawling
import distinguisher
import app_repository
import notifier

from apscheduler.schedulers.background import BackgroundScheduler
import time

interval_sec = 600

def repeat_job():
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(main, 'interval', seconds=interval_sec, id="test_interval_1")


def main():
    print(u"running jungo-car-app!")
    data = crawling.crawling()
    distinguished_cars = distinguisher.distinguish(data)
    app_repository.update_leave_and_deleted(distinguished_cars)
    notifier.notify(distinguished_cars)

main()
repeat_job()

while True:
    time.sleep(interval_sec)
