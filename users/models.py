from enum import IntEnum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.time_mixin import TimeMixin


class UserGender(IntEnum):
    FEMAIL, MAIL, UNKONWN = 0, 1, 2

    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))


# Create your models here.
class Users(TimeMixin):
    name = models.CharField(null=False, blank=False, max_length=200, unique=False)
    pwd = models.CharField(null=False, blank=False, max_length=200, unique=False)
    email = models.EmailField(max_length=200, unique=False)
    phone = models.CharField(max_length=11, unique=True)
    age = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], default=0)
    address = models.CharField(max_length=200, default="unkown address")
    gender = models.SmallIntegerField(choices=UserGender.choices(), default=2)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        db_table = 'users'
        verbose_name = 'users'
        verbose_name_plural = 'users'
