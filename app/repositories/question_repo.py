from app.models.question import Question

class QuestionRepository:
    @staticmethod
    async def read_one_question():
        return await Question.all() 