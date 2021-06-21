# Generated by Django 3.1.1 on 2020-09-26 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('calls_left', models.IntegerField(default=10)),
                ('active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='recent_otp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('date', models.FloatField(default=1601149819.0595267)),
            ],
        ),
    ]