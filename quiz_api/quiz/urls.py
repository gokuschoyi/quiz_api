from django.urls import path
from .views import QuizDetailView, get_lessons, get_quizzes_for_lesson, get_questions_for_quiz, evaluate_answers

urlpatterns = [
    path("get_lessons", get_lessons, name="get-lessons"),
    path("get_quiz/<int:user_id>/<int:lesson_id>/", get_quizzes_for_lesson, name="get-quiz"),
    path("get_questions/<int:quiz_id>/", get_questions_for_quiz, name="get-questions"),
    path("evaluate_quiz", evaluate_answers, name="evaluate-quiz"),
    # path("get_quiz/<int:quiz_id>/", QuizDetailView.as_view(), name="quiz-detail"),
]
