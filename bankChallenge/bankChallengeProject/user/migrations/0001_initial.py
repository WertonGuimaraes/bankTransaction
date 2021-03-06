# Generated by Django 3.1.7 on 2021-03-26 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=254)),
                ('current_balance', models.FloatField()),
                ('old_balance', models.FloatField()),
                ('value', models.FloatField()),
                ('transaction_type', models.CharField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='user.user')),
            ],
        ),
    ]
