# Generated by Django 3.1.7 on 2021-03-25 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_operation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='transactionType',
            field=models.CharField(default='credit', max_length=254),
            preserve_default=False,
        ),
    ]
