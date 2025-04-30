from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger



from backend.services.stock_service import make_stock_charts

scheduler = AsyncIOScheduler()

def start_scheduler():
    trigger = CronTrigger(hour=7, minute=00, timezone='Asia/Seoul')
    scheduler.add_job(make_stock_charts, trigger, misfire_grace_time=3000)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()