import re

from django.db import models
from slugify import slugify


class AbstractNameSlugModel(models.Model):
    """
    Абстрактный класс, для моделей с полями:
    * name
    * slug (уникальный)

    Содержит измененую логику для сохранение в БД:
    если slug пустой - генерирует на основе name уникальное значение.
    Если в БД slug используется - добавляет после него номер.
    Итоговое название имеет вид `{gen_slug}-{0}`
    """

    name = models.CharField(
        verbose_name='Наименование',
        max_length=127,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=163,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ['name', 'slug']

    def save(self, *args, **kwargs):
        is_new_object = not bool(self.pk)
        objects = self.__class__.objects

        if (
            is_new_object
            or self.name != objects.filter(pk=self.pk).first.name
        ):
            base_slug = slugify(self.name)
            # Получаем все slug, начинающиеся с `base_slug`
            existing_slags = objects.filter(
                slug__startswith=base_slug
            ).values_list('slug', flat=True)

            max_suffix = None
            for slug in existing_slags:
                # Ищем слаги для base-slug-`count`
                match = re.search(r'-(\d+)$', slug)
                if match:
                    suffix = int(match.group(1))
                    if max_suffix is None or suffix > max_suffix:
                        max_suffix = suffix

            if max_suffix is not None:
                new_slug = f'{base_slug}-{max_suffix + 1}'
            else:
                new_slug = base_slug

            self.slug = new_slug

        super().save(*args, **kwargs)


class AbstractCategoryModel(AbstractNameSlugModel):
    """Абстрактная модель категорий с полем image."""
    image = models.ImageField(
        verbose_name='Путь до картинки',
        blank=True,
        upload_to='category/image/'
    )

    class Meta(AbstractNameSlugModel.Meta):
        abstract = True
