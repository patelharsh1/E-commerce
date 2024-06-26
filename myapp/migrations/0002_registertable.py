# Generated by Django 5.0.2 on 2024-02-16 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='registertable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.BigIntegerField()),
                ('password', models.CharField(max_length=40)),
                ('role', models.CharField(max_length=40)),
                ('profilepic', models.ImageField(upload_to='photos')),
            ],
        ),
    ]
