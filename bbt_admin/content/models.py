from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars, urlizetrunc
from mptt.models import MPTTModel, TreeForeignKey


class Content(MPTTModel):
    title = models.CharField('Заголовок', max_length=256)
    proof_link = models.URLField(
        'Ссылка на программу на сайте',
        max_length=2048,
        blank=True
    )
    program = models.TextField(
        'Содержание программы',
        blank=True
    )
    date_on = models.DateField(
        'Дата начала программы',
        blank=True,
        null=True
    )
    date_off = models.DateField(
        'Дата завершения программы',
        blank=True,
        null=True
    )
    media = models.URLField('Ссылка на медиа', blank=True)
    file_id = models.CharField(
        'ID фото в базе Телеграмма',
        max_length=512,
        blank=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='child',
        db_index=True,
        verbose_name='родительский контент'
    )

    @property
    def display_program(self):
        return truncatechars(self.program, 50)
    display_program.fget.short_description = 'Содержание программы'

    @property
    def display_proof_link(self):
        return urlizetrunc(self.proof_link, 20)
    display_proof_link.fget.short_description = 'Ссылка на программу на сайте'

    @property
    def display_media(self):
        return urlizetrunc(self.media, 20)
    display_media.fget.short_description = 'Ссылка на медиа'

    @property
    def display_file_id(self):
        return truncatechars(self.file_id, 20)
    display_file_id.fget.short_description = 'ID фото в базе Телеграмма'

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'title']]
        verbose_name = 'контент'
        verbose_name_plural = 'контент'

    def __str__(self):
        return self.title

    def clean(self):
        if self.date_on and self.date_off and self.date_on > self.date_off:
            raise ValidationError(
                {
                    'date_on': ('Дата начала программы должна быть '
                                'меньше даты завершения программы'),
                    'date_off': ('Дата завершения программы должна быть '
                                 'больше даты начала программы')
                }
            )


class ContentLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='history'
    )
    content = models.ForeignKey(
        Content,
        verbose_name='контент',
        related_name='history',
        on_delete=models.CASCADE
    )
    datetime_on = models.DateTimeField(
        verbose_name='Дата и время отправки',
        auto_now_add=True
    )
    date_back = models.DateTimeField(
        verbose_name='Дата и время перехода назад',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-datetime_on']
