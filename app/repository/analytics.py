from collections import defaultdict
from typing import List, Dict

from sqlalchemy import select, func

from app.db.db_connect import get_db
from app.db.models import Result, User, Quiz
from app.services.action_services import actions
from app.services.exceptions import ActionPermissionException


class AnalyticsRepository:

    async def get_user_analytics(self, user_id: int) -> Dict:
        return {"user_id": user_id,
                "rating": await self.__calculate_total_user_rating(user_id)}

    async def get_user_quizzes_analytics(self, current_user: User) -> Dict:
        results = await self.__get_quiz_results_for_user(current_user.id)
        quiz_scores = defaultdict(list)

        for result in results:
            quiz_id = result.result_quiz_id
            completion_time = result.created_at
            correct_count = result.result_right_count
            total_count = result.result_total_count

            average_score = format(correct_count / total_count * 100, ".2f")

            quiz_result = {"quiz_id": quiz_id,
                           "completion_time": completion_time,
                           "average_score": average_score}
            quiz_scores["results"].append(quiz_result)

        return quiz_scores

    async def get_latest_quiz_completion_times_for_user(self, current_user: User) -> Dict:
        async for session in get_db():
            query = select(
                Quiz.id.label('quiz_id'),
                Quiz.quiz_name,
                func.max(Result.created_at).label('last_attempt_time')
            ).join(
                Result,
                (Quiz.id == Result.result_quiz_id) & (Result.result_user_id == current_user.id)
            ).group_by(
                Quiz.id,
                Quiz.quiz_name
            )

            result = await session.execute(query)
            results = result.all()
            quiz_time = defaultdict(list)

            for result in results:
                quiz_data = {"quiz_id": result.quiz_id,
                             "quiz_name": result.quiz_name,
                             "last_attempt_time": result.last_attempt_time}

                quiz_time["quizzes"].append(quiz_data)
            return quiz_time

    async def get_users_scores_analytics_in_company(self, company_id: int, current_user: User) -> Dict:
        async for session in get_db():
            if (await actions.validate_user_is_owner(current_user.id, company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, company_id, session)):
                query = select(
                    User.user_firstname,
                    User.user_lastname,
                    Quiz.quiz_name,
                    Result.result_user_id,
                    Result.result_quiz_id,
                    Result.result_right_count,
                    Result.result_total_count,
                    Result.created_at
                ).join(
                    User,
                    User.id == Result.result_user_id
                ).join(
                    Quiz,
                    Quiz.id == Result.result_quiz_id
                ).filter(
                    Result.result_company_id == company_id
                ).order_by(
                    Result.created_at
                )

                result = await session.execute(query)
                results = result.all()

                user_results = []

                for result in results:
                    user_result = {
                        "user_id": result.result_user_id,
                        "user_firstname": result.user_firstname,
                        "user_lastname": result.user_lastname,
                        "quiz_id": result.result_quiz_id,
                        "quiz_name": result.quiz_name,
                        "score": format(result.result_right_count / result.result_total_count * 100, ".2f"),
                        "completion_time": result.created_at
                    }

                    user_results.append(user_result)

                return {"users_results": user_results}
            raise ActionPermissionException

    async def get_user_average_scores_in_company_over_time(self, user_id: int, company_id: int,
                                                           current_user: User) -> Dict:
        async for session in get_db():
            if (await actions.validate_user_is_owner(current_user.id, company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, company_id, session)):
                query = select(
                    Quiz.id.label('quiz_id'),
                    Quiz.quiz_name,
                    func.avg(Result.result_right_count / Result.result_total_count * 100).label('average_score'),
                    Result.created_at
                ).join(
                    Quiz,
                    Quiz.id == Result.result_quiz_id
                ).filter(
                    Result.result_user_id == user_id,
                    Quiz.quiz_company_id == company_id
                ).group_by(
                    Quiz.id,
                    Quiz.quiz_name,
                    Result.created_at
                ).order_by(
                    Quiz.id,
                    Result.created_at
                )
                result = await session.execute(query)
                results = result.all()
                user_average_scores = defaultdict(list)
                for row in results:
                    quiz_data = {
                        "user_id": user_id,
                        "quiz_id": row.quiz_id,
                        "quiz_name": row.quiz_name,
                        "score": format(row.average_score, ".2f"),
                        "completion_time": row.created_at
                    }
                    user_average_scores["quizzes_result"].append(quiz_data)
                return user_average_scores
            raise ActionPermissionException

    async def get_users_last_completion_time_in_company(self, company_id: int, current_user: User) -> Dict:
        async for session in get_db():
            if (await actions.validate_user_is_owner(current_user.id, company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, company_id, session)):
                query = select(
                    User.id,
                    User.user_firstname,
                    User.user_lastname,
                    func.max(Result.created_at).label('last_completion_time')
                ).join(
                    Result,
                    User.id == Result.result_user_id
                ).filter(
                    Result.result_company_id == company_id
                ).group_by(
                    User.id,
                    User.user_firstname,
                    User.user_lastname
                )

                result = await session.execute(query)
                results = result.all()

                user_completion_times = []

                for row in results:
                    user_completion_time = {
                        "user_id": row.id,
                        "user_firstname": row.user_firstname,
                        "user_lastname": row.user_lastname,
                        "last_completion_time": row.last_completion_time
                    }

                    user_completion_times.append(user_completion_time)

                return {"users_last_completion_time": user_completion_times}
            raise ActionPermissionException

    async def __calculate_total_user_rating(self, user_id: int) -> float:
        quiz_results = await self.__get_quiz_results_for_user(user_id)

        total_correct_count = 0.0
        total_count = 0

        for result in quiz_results:
            total_correct_count += result.result_right_count
            total_count += result.result_total_count

        return format(total_correct_count / total_count * 100, ".2f") if total_count > 0 else 0.00

    async def __get_quiz_results_for_user(self, user_id: int) -> List:
        async for session in get_db():
            query = select(Result).where(Result.result_user_id == user_id)
            return (await session.execute(query)).scalars().all()
