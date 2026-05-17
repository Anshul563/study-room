from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from app.ai.auto_summary import (
    generate_auto_summaries
)

scheduler = BackgroundScheduler()

scheduler.add_job(
    generate_auto_summaries,
    "interval",
    minutes=5
)

def start_scheduler():

    scheduler.start()