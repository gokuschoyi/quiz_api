from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lesson, Quiz, Score, Question, Choice
from .serializer import AnswerEvaluationSerializer


@api_view(["GET"])
def get_lessons(request):
    try:
        lessons = Lesson.objects.all()
        lesson_list = []
        for lesson in lessons:
            lesson_list.append(
                {
                    "id": lesson.id,
                    "title": lesson.title,
                    "content": lesson.content,
                }
            )
        return Response(lesson_list, status=status.HTTP_200_OK)
    except Lesson.DoesNotExist:
        return Response({"message": "No lessons found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_quizzes_for_lesson(request, user_id, lesson_id):
    print("user id", user_id)
    try:
        completed = Score.objects.filter(user_id=user_id).values("quiz_id", "score")
        # print("Completed", completed)
        completed_dict = {score["quiz_id"]: score["score"] for score in completed}
        print("Completed", completed_dict)

        quizzes = Quiz.objects.filter(lesson=lesson_id)
        quiz_list = []
        for quiz in quizzes:
            total_questions = Question.objects.filter(quiz_id=quiz.id)
            # print(len(total_questions))
            quiz_data = {
                "id": quiz.id,
                "title": quiz.title,
                "completed":False,
                "score":0,
                "total":len(total_questions)
            }
            if quiz.id in completed_dict:
                quiz_data["completed"] = True
                quiz_data["score"] = completed_dict[quiz.id]
            quiz_list.append(quiz_data)
        return Response(quiz_list, status=status.HTTP_200_OK)
    except Quiz.DoesNotExist:
        return Response({"message": "No quizzes found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_questions_for_quiz(request, quiz_id):
    try:
        questions = Question.objects.filter(quiz=quiz_id)
        question_list = []
        for question in questions:
            question_list.append(
                {
                    "id": question.id,
                    "text": question.text,
                    "question_type": question.question_type,
                    "choices": [
                        {
                            "id": choice.id,
                            "text": choice.text,
                            # "is_correct": choice.is_correct,
                        }
                        for choice in question.choices.all()
                    ],
                }
            )
        return Response(question_list, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response({"message": "No questions found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def evaluate_answers(request):
    # print("DATA", request.data["answers"])
    answers = request.data["answers"]
    answer_serializer = AnswerEvaluationSerializer(data=answers, many=True)

    if not answer_serializer.is_valid():
        return Response({"error":answer_serializer.errors,"messge":"Please select all the answers"}, status=status.HTTP_400_BAD_REQUEST)

    score = 0
    total_questions = len(answer_serializer.validated_data)

    for answer in answer_serializer.validated_data:
        question = Question.objects.get(id=answer["question_id"])
        selected_answers = answer["selected_answers"]
        correct_choices = question.choices.filter(is_correct=True).values_list("text", flat=True)

        # print("Selected answers", selected_answers, "Correct choices", correct_choices)

        if set(selected_answers) == set(correct_choices):
            score += 1

    score_data = {
        "score": score,
        "quiz_id": request.data["quiz_id"],
        "user_id": request.data["user_id"],
    }

    Score.objects.create(**score_data)

    return Response({"score": score, "total_questions": total_questions, "evaluated":True}, status=status.HTTP_200_OK)
