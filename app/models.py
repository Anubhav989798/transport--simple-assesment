from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='question'

class Answer(models.Model):
    answer=models.TextField()
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='answer'