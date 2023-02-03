from django.db import models

# Create your models here.

class Question(models.Model):
    sno=models.AutoField(primary_key=True)
    ques=models.CharField(max_length=200)
    opt1=models.CharField(max_length=200)
    opt2=models.CharField(max_length=200)
    opt3=models.CharField(max_length=200)
    opt4=models.CharField(max_length=200)
    correct=models.CharField(max_length=200)
    correct_opt=models.CharField(max_length=10)


class Task_Result(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    s_range=models.IntegerField()
    e_range=models.IntegerField()
    test_status=models.CharField(max_length=50,default='False')
    test_unlock=models.CharField(max_length=50,default="False")
    points=models.IntegerField(default=0)


