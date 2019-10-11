#!/usr/bin/env python
# encoding=utf-8

import crawling
import distinguisher
import app_repository
import notifier

from apscheduler.schedulers.background import BlockingScheduler
import time

working_interval_sec = 600
health_check_sec = 1


def repeat_job():
    sched = BlockingScheduler()
    sched.start()
    sched.add_job(main, 'interval', seconds=working_interval_sec, id="test_interval_1")


def main():
    print(u"running jungo-car-app!")
    data = crawling.crawling()
    distinguished_cars = distinguisher.distinguish(data)
    app_repository.update_leave_and_deleted(distinguished_cars)
    notifier.notify(distinguished_cars)


main()
repeat_job()

while True:
    print("i am alive!")
    time.sleep(health_check_sec)
