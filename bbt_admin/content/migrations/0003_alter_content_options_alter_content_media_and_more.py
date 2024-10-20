import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'verbose_name': 'контент', 'verbose_name_plural': 'контент'},
        ),
        migrations.AlterField(
            model_name='content',
            name='media',
            field=models.URLField(blank=True, verbose_name='Ссылка на медиа'),
        ),
        migrations.AlterField(
            model_name='content',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child', to='content.content', verbose_name='родительский контент'),
        ),
        migrations.AlterField(
            model_name='content',
            name='program',
            field=models.TextField(blank=True, verbose_name='Содержание программы'),
        ),
        migrations.AlterField(
            model_name='content',
            name='proof_link',
            field=models.URLField(blank=True, max_length=2048, verbose_name='Ссылка на программу на сайте'),
        ),
        migrations.AlterField(
            model_name='contentlog',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='content.content', verbose_name='контент'),
        ),
        migrations.AlterField(
            model_name='contentlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
