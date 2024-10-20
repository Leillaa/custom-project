from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0003_alter_content_options_alter_content_media_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')),
                ('file_id', models.CharField(max_length=512, verbose_name='ID фото в базе Телеграмма')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='content.content', verbose_name='контент')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'ordering': ['-datetime_on'],
            },
        ),
    ]
