# Generated by Django 5.1.1 on 2024-10-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_canteen_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='nickname',
            field=models.CharField(default='FMIPA', max_length=10),
            preserve_default=False,
        ),
    ]
