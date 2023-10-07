from pytz import timezone

from app.utils.tasks import check_quiz_completion
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler_app = AsyncIOScheduler(timezone=timezone('Europe/Kiev'))


@scheduler_app.scheduled_job("cron", hour=0, minute=0)
async def scheduled_job():
    await check_quiz_completion()
