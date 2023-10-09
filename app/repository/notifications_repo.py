from typing import Optional

from fastapi import HTTPException, status

from app.db.models import User, Quiz, Notification


class NotificationRepository:

    async def create_quiz_notification(self,
                                       user_id: int,
                                       quiz_id: int,
                                       session,
                                       text: str = None) -> Optional[Notification]:
        user = await session.get(User, user_id)
        quiz = await session.get(Quiz, quiz_id)
        if not (user and quiz):
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User or quiz not found")
        if text is None:
            notification_text = f"Dear User. We invite you to complete a new quizz: {quiz.quiz_name}"
        else:
            notification_text = text
        notification = Notification(
            user_id=user_id,
            text=notification_text
        )
        session.add(notification)
        await session.commit()
        return notification
