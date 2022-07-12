from django.db import models

from ..users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Автор рецепта'
    )
    title = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        verbose_name='Изображение блюда'
    )
    description = models.TextField(
        'Описание',
        help_text='Введите текст описания рецепта'
    )
    cooking_time = models.PositiveIntegerField('Время приготовления')
