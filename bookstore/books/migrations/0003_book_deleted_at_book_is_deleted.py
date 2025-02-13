# Generated by Django 5.1.6 on 2025-02-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
