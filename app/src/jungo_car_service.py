#!/usr/bin/env python
# encoding=utf-8
import traceback
import os
import sys
from apscheduler.schedulers.background import BlockingScheduler
import datetime
import pytz

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from crawler import crawler
from notifier import notifier
from distinguisher import distinguisher
from repository import app_repository
from model.division_state_cars import DivisionStateCars
from crawler.exceptions.fail_crawl import FailCrawl

working_interval_sec = 60 * 1


def init_notify():
    notifier.hello_notify()


def start_scheduled_job():
    sched = BlockingScheduler()
    sched.add_job(main, 'interval',
                  seconds=working_interval_sec, id="real_time_1")
    sched.start()


def main():
    print(str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y/%m/%d %H:%M:%S")))
    try:
        data = crawler.crawler()
        dsc: DivisionStateCars = distinguisher.distinguish(data)
        app_repository.update_leave_and_deleted(dsc)
        notifier.notify(dsc)
    except FailCrawl as e:
        print("크롤링 중 문제가 발생했습니다.", e)
        pass
    except Exception as e:
        print("작업 중 예상치 못한 문제가 발생함.", e)
        traceback.print_exc()
        pass
    print("루프 끝")
    

if __name__ == "__main__":
    print(u"Running jungo-car-app!")
    init_notify()
    print(u"Notifier is successfully working!")
    main()
    start_scheduled_job()

# def test():
#     app_repository    
    
# test()