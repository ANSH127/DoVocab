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
    correct_opt=models.IntegerField()

    def __str__(self):
        return "sno "+str(self.sno)+" Question "+self.ques


class Task_Result(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    s_range=models.IntegerField()
    e_range=models.IntegerField()

class userdetail(models.Model):
    user=models.CharField(max_length=100,default="")
    sno=models.AutoField(primary_key=True)
    task=models.ForeignKey(Task_Result,on_delete=models.CASCADE)
    test_status=models.CharField(max_length=50,default='False')
    test_unlock=models.CharField(max_length=50,default="False")
    points=models.IntegerField(default=0)
    user_choosen=models.CharField(max_length=50,default='')



