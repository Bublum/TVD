# Generated by Django 2.1.1 on 2019-05-01 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Dashboard', '0003_auto_20190405_0438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='input',
            old_name='model',
            new_name='file',
        ),
        migrations.AddField(
            model_name='input',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]