from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from accounts.models import User


class Question(models.Model):
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}, {self.body[:75] + (self.body[75:] and '..')}"

    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content_type = models.ForeignKey(ContentType, related_name="content_type_question", on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField('관련 데이터 번호')
    content_object = GenericForeignKey('content_type', 'object_id')
    body = models.TextField('내용')
    is_complete = models.BooleanField('답변완료여부', default=False)


class Answer(models.Model):
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}, {self.body[:75] + (self.body[75:] and '..')}"

    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField('내용')
