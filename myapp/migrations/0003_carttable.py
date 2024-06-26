# Generated by Django 5.0.2 on 2024-02-28 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_registertable'),
    ]

    operations = [
        migrations.CreateModel(
            name='carttable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('totalamount', models.IntegerField()),
                ('cartstatus', models.IntegerField()),
                ('orderid', models.IntegerField()),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.productdetail')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.registertable')),
            ],
        ),
    ]
