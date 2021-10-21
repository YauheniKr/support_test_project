from django.contrib.auth.models import AbstractUser
from django.db import models

from support_api.choices import Role, Status
from support_api.managers import UserManager


class User(AbstractUser):
    role = models.TextField(verbose_name='role', choices=Role.choices, default='user')

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == Role.ADMIN


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.TextField(verbose_name='status', choices=Status.choices, default='open')

    class Meta:
        ordering = ['-pub_date', ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created', ]
