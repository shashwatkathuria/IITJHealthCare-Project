# Generated by Django 2.1.5 on 2019-04-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalStore', '0005_medicine_photoid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='photoId',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
