# Generated by Django 4.0.3 on 2022-04-14 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0021_auto_discountpct'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='auto',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]