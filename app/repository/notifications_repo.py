from fastapi import HTTPException, status

from app.db.db_connect import get_db
from app.db.models import User, Quiz, Notification


class NotificationRepository:

    async def create_quiz_notification(self, user_id, quiz_id, session):
        user = await session.get(User, user_id)
        quiz = await session.get(Quiz, quiz_id)
        if user and quiz:
            notification = Notification(
                user_id=user_id,
                text=f"Dear User. We invite you to complete a new quizz: {quiz.quiz_name}"
            )
            session.add(notification)
            await session.commit()
            return notification
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User or quiz not found")

