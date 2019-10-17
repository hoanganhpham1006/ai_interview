from django.db import models
from django.conf import settings
# Create your models here.
# class User(models.Model):
#   user_id = models.AutoField(primary_key=True)
#   username = models.CharField(max_length=100)
#   password = models.CharField(max_length=100)

class Question(models.Model):
  question_id = models.AutoField(primary_key=True)
  question_content = models.TextField()
  question_category = models.IntegerField()
  question_type = models.IntegerField()
  question_sound_file = models.FilePathField(path="/quesion_sound/")

class Answer(models.Model):
  answer_id = models.AutoField(primary_key=True)
  answer_content = models.TextField()

class Resume(models.Model):
  resume_id = models.AutoField(primary_key=True)
  # resume_created_by = models.ForeignKey('User', on_delete=models.CASCADE)
  resume_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  resume_name = models.CharField(max_length=100)
  resume_dob = models.DateTimeField()
  resume_mobile = models.TextField()
  resume_email = models.EmailField()
  resume_additional_information = models.TextField()
  resume_link = models.TextField()

class QuestionAnwser(models.Model):
  qa_id = models.AutoField(primary_key=True)
  question = models.ForeignKey('Question', on_delete=models.CASCADE)
  answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

class Test(models.Model):
  test_id = models.AutoField(primary_key=True)
  test_name = models.CharField(max_length=100)
  # test_created_by = models.ForeignKey('User', on_delete=models.CASCADE)
  test_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Interview(models.Model):
  interview_id = models.AutoField(primary_key=True)
  interview_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  # interview_created_by = models.ForeignKey('User', on_delete=models.CASCADE)
  resume = models.ForeignKey('Resume', on_delete=models.CASCADE)
  interview_link = models.TextField()
  interview_result = models.TextField()
  interview_test = models.ForeignKey('Test', on_delete=models.CASCADE)
  interview_videorecord_file = models.FilePathField(path="/interview_video/")
  interview_conversation_text = models.TextField()


class QuestionTest(models.Model):
  qt_id = models.AutoField(primary_key=True)
  question = models.ForeignKey('Question', on_delete=models.CASCADE)
  test = models.ForeignKey('Test', on_delete=models.CASCADE)
  question_index = models.IntegerField()