from apscheduler.schedulers.blocking import BlockingScheduler
from update import update_stats

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=15, minutes=40)
def scheduled_job():
    print('This job updates stats daily at 11 PM.')
    update_stats()

sched.start()