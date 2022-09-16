# Generated by Django 4.1.1 on 2022-09-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=40)),
                ('account_number', models.PositiveIntegerField()),
                ('total_assessts', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
    ]
