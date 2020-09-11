from django.contrib.auth.models import UserManager
from django.db import models


class BaseManagerMixin:
    def get_queryset(self):
        return super(BaseManagerMixin, self).get_queryset().only('id')


class UserModelManager(BaseManagerMixin, UserManager):
    pass


class BaseManager(BaseManagerMixin, models.Manager):
    pass