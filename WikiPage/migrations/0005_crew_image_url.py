# Generated by Django 5.1.3 on 2024-12-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WikiPage', '0004_remove_arc_image_remove_chapter_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crew',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
