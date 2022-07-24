from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=55,
        blank=False,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=55,
        blank=False,
        unique=True
    )
    color = models.CharField('Цвет тега в HEX', max_length=7)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=100,
        blank=False
    )
    count = models.PositiveIntegerField()
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=100,
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredients'
            )
        ]


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
        db_index=True
    )
    title = models.CharField(
        'Название рецепта',
        max_length=250,
        blank=False
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/',
        blank=True,
    )
    description = models.TextField(
        'Описание',
        help_text='Введите описания рецепта',
        blank=False
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        blank=False
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipe',
        db_index=True,
        verbose_name='Тег'
    )


    class Meta:
        ordering = ['-pk']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
