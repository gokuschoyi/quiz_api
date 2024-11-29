from django.contrib import admin
from .models import Lesson, Quiz, Score, Question, Choice

# Register your models here.

admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Score)
admin.site.register(Question)
admin.site.register(Choice)
