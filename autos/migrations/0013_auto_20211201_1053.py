# Generated by Django 3.1.7 on 2021-12-01 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0012_auto_20211130_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='auto',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='auto',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='auto',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='auto',
            name='image6',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
