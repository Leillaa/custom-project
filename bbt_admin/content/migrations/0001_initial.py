import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('proof_link', models.URLField(max_length=2048, verbose_name='Ссылка на программу на сайте')),
                ('program', models.TextField(verbose_name='Содержание программы')),
                ('date_on', models.DateField(blank=True, null=True, verbose_name='Дата начала программы')),
                ('date_off', models.DateField(blank=True, null=True, verbose_name='Дата завершения программы')),
                ('media', models.URLField(blank=True, null=True, verbose_name='Ссылка на медиа')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Контент',
                'verbose_name_plural': 'Контент',
            },
        ),
        migrations.CreateModel(
            name='ContentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='content.content', verbose_name='Контент')),
            ],
            options={
                'ordering': ['-datetime_on'],
            },
        ),
    ]
