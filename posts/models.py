from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)  # 삭제되면
    created = models.DateTimeField(auto_now_add=True)  # 생성시간 자동생성

    class Meta:
        ordering = ['-created']  # 게시 순으로 정렬


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)  # User와 관계
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post와 관계
