from apscheduler.schedulers.blocking import BlockingScheduler
from update import update_stats

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=16, minute=55)
def scheduled_job():
    print('This job updates stats daily at 11 PM.')
    update_stats()

sched.start()