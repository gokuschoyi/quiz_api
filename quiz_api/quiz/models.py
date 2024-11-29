from django.db import models
from authorization.models import CustomUser


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="quizzes", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.lesson.title}"


class Question(models.Model):
    QUESTION_TYPES = [
        ("single", "Single Answer"),
        ("multi", "Multiple Answers"),
        ("select_word", "Select Words"),
    ]
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=50)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Score(models.Model):
    user = models.ForeignKey(CustomUser, related_name="scores", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="scores", on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score: {self.score} - User: {self.user.email} - Quiz: {self.quiz.title}"
