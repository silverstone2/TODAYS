# Generated by Django 4.1.4 on 2022-12-23 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CafeList',
            fields=[
                ('cafename', models.CharField(max_length=50)),
                ('gu', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('dong', models.CharField(max_length=50)),
                ('review', models.CharField(max_length=50)),
                ('bookmark', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cafe_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mylike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('cafename', models.CharField(max_length=50)),
                ('addr', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('review', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'mylike',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mybookmark',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('cafename', models.CharField(max_length=50)),
                ('addr', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('memo', models.CharField(max_length=250)),
            ],
        ),
    ]