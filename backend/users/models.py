from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    password = models.CharField(
        max_length=55,
        blank=False,
        verbose_name='Пароль'
    )
    username = models.CharField(
        max_length=75,
        unique=True,
        blank=False,
        verbose_name='Логин'
    )
    email = models.EmailField(
        max_length=90,
        unique=True,
        blank=False,
        verbose_name='Почта'
    )
    first_name = models.CharField(
        max_length=55,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=55,
        blank=False,
        verbose_name='Фамилия'
    )
    is_administrator = models.BooleanField('Администратор', default=False)
    is_blocked = models.BooleanField('Блокировка', default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_administrator

    @property
    def is_block(self):
        return self.is_blocked


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow')
        ]
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'
