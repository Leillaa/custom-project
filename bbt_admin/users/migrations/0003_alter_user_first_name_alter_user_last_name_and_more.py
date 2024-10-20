from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_date_joined_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default='empty', max_length=64, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default='empty', max_length=64, verbose_name='Фамилия'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, default='empty', max_length=128, verbose_name='Пароль'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default='empty', max_length=32, verbose_name='Телеграм никнейм'),
            preserve_default=False,
        ),
    ]
