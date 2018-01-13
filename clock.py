from apscheduler.schedulers.blocking import BlockingScheduler
from update import update_stats

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=1, minute=37)
def scheduled_job():
    print('This job updates stats daily at 11 PM.')
    update_stats()

sched.start()