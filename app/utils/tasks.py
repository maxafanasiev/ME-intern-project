from datetime import datetime, timedelta

from sqlalchemy import select

from app.db.db_connect import get_db
from app.db.models import User, Quiz
from app.repository.quizzes import QuizRepository as QuizRepo
from app.repository.notifications_repo import NotificationRepository as Notify


async def check_quiz_completion():
    async for session in get_db():
        users = (await session.execute(select(User))).scalars().all()
        quizzes = (await session.execute(select(Quiz))).scalars().all()

        for user in users:
            for quiz in quizzes:
                last_completion_time = await QuizRepo().get_last_completion_time(user.id, quiz.id, session)

                min_time = datetime.utcnow() - timedelta(days=quiz.quiz_frequency)

                if last_completion_time is None:
                    pass
                elif last_completion_time < min_time:
                    await Notify().create_quiz_notification(user.id, quiz.id, session,
                                                            text=f"Complete the quiz: {quiz.quiz_name}")
