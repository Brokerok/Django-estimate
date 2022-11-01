from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('\n'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    tariff = models.BooleanField(default=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    number = models.PositiveSmallIntegerField(null=False, default=1)
    status = models.CharField(max_length=20, default='in progress')

    def __str__(self):
        return str(self.pk)


class Pdf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    order = models.PositiveSmallIntegerField(null=False, default=1)
    pdf = models.FileField(null=True, blank=True, upload_to='data/')

    def __str__(self):
        return str(self.user)

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)


