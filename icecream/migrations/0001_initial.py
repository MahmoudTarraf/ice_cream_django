# Generated by Django 5.0.3 on 2024-03-16 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IceCreamModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=50)),
                ('details', models.TextField()),
                ('category', models.CharField(max_length=50)),
            ],
        ),
    ]
