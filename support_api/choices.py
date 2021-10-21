from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class Status(models.TextChoices):
    OPEN = 'Open'
    IN_PROGRESS = 'In progress'
    CLOSE = 'Close'
