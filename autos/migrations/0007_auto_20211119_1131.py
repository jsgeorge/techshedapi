# Generated by Django 3.1.7 on 2021-11-19 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0006_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='color',
            field=models.CharField(blank=True, choices=[('White', 'White'), ('Red', 'Red'), ('Blue', 'Blue'), ('Silver', 'Silver'), ('Green', 'Green'), ('Black', 'Black')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='auto',
            name='condition',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Used', 'Used'), ('Refurbished', 'Refurbished')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='auto',
            name='doors',
            field=models.CharField(blank=True, choices=[('2', '2'), ('3', '3'), ('4', '4')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='auto',
            name='fueltype',
            field=models.CharField(blank=True, choices=[('Gasoline', 'Gasoline'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='auto',
            name='owners',
            field=models.CharField(default='1', max_length=10),
        ),
        migrations.AlterField(
            model_name='auto',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
