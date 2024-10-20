from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_content_options_alter_content_media_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='file_id',
            field=models.CharField(blank=True, max_length=512, verbose_name='ID фото в базе Телеграмма'),
        ),
    ]
