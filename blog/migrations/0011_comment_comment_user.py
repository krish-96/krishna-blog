# Generated by Django 2.2.9 on 2020-05-22 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_public_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.Author'),
            preserve_default=False,
        ),
    ]