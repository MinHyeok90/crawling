#!/usr/bin/env python
# encoding=utf-8

import crawling
import distinguisher
import app_repository
import notifier

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import time

interval_sec = 600

def repeat_job():
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(main, 'interval', seconds=interval_sec, id="test_interval_1")


def main():
    print(u"running jungo-car-app!")
    data = crawling.crawling()
    distinguished_data = distinguisher.distinguish(data)
    app_repository.save(distinguished_data)
    notifier.notify(distinguished_data)

main()
repeat_job()

while True:
    time.sleep(interval_sec)
