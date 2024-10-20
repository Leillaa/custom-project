from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_photolog"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PhotoLog",
        ),
    ]
