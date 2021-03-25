# Generated by Django 3.1.7 on 2021-03-25 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_operation_created_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='created_datetime',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='operation',
            name='description',
            field=models.CharField(default='descricao default', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]