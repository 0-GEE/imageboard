# Generated by Django 4.0.6 on 2022-07-28 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0003_alter_posting_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='file',
            field=models.ImageField(upload_to='imageboard'),
        ),
    ]
