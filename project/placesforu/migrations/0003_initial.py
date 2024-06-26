# Generated by Django 4.2.11 on 2024-04-28 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('placesforu', '0002_delete_uploadimagemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('country_iso3', models.CharField(max_length=3)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
