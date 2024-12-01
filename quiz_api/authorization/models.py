from django.db import models

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.email