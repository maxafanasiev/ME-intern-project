from operator import and_

from sqlalchemy import select

from app.db.models import Question, Result


class Results:

    async def get_all_questions_in_quiz(self, quiz_id, session):
        query = select(Question).where(Question.question_quiz_id == quiz_id)
        res = await session.execute(query)
        return res.scalars().all()

    async def calculate_correct_answers(self, answers_list, questions_list):
        question_correct_answers = 0
        for answer in answers_list["answers"]:
            for question in questions_list:
                if (question.id == answer["question_id"]
                        and answer["answer"] == question.question_correct_answers):
                    question_correct_answers += 1
        return question_correct_answers

    async def calculate_user_average_score_in_company(self, user_id, company_id, session):
        query = select(Result).where(and_(Result.result_user_id == user_id, Result.result_company_id == company_id))
        res = await session.execute(query)
        results = res.scalars().all()

        average_score = await self.__get_average_score(results)
        return {"user_id": user_id,
                "company_id": company_id,
                "average_score": format(average_score, '.2f')}

    async def calculate_user_average_score_global(self, user_id: int, session):
        query = select(Result).where(Result.result_user_id == user_id)
        res = await session.execute(query)
        results = res.scalars().all()
        average_score = await self.__get_average_score(results)
        return {"user_id": user_id,
                "average_score": format(average_score, '.2f')}

    async def __get_average_score(self, results: list):
        total_correct_answers = 0
        total_questions_answered = 0

        for result in results:
            total_correct_answers += result.result_right_count
            total_questions_answered += result.result_total_count

        if total_questions_answered == 0:
            return 0.0

        average_score = total_correct_answers / total_questions_answered * 100
        return average_score


results = Results()
