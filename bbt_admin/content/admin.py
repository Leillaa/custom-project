from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Content, ContentLog


@admin.register(Content)
class ContentAdmin(MPTTModelAdmin):
    list_display = (
        'pk',
        'title',
        'display_proof_link',
        'display_program',
        'date_on',
        'date_off',
        'display_media',
        'display_file_id',
        'parent'
    )
    list_display_links = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(ContentLog)
class ContentLogAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'content',
        'datetime_on',
        'date_back'
    )
    search_fields = ('user__telegram_id',)
    empty_value_display = '-пусто-'

    def has_add_permission(self, request):
        return False
