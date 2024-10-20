from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_merge_20220715_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentlog',
            name='date_back',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время перехода назад'),
        ),
    ]
