from django.contrib import admin


class AbstractNameSlugAdmin(admin.ModelAdmin):
    """Заготовка под поля со слагом и именем."""

    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    ordering = ['name']


class AbstractCategoryAdmin(AbstractNameSlugAdmin):
    """Заготовка под категории."""

    list_display = AbstractNameSlugAdmin.list_display + ['image']
