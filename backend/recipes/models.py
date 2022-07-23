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


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=100,
        blank=False
    )
    count = models.PositiveIntegerField(
        'Количество ингредиентов',
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=100
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    title = models.CharField(
        'Название рецепта',
        max_length=250,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/',
        blank=True,
    )
    description = models.TextField(
        'Описание',
        help_text='Введите описания рецепта'
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
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
