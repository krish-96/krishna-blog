# Generated by Django 2.2.9 on 2020-05-22 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_author_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Public_Post',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blog.post',),
        ),
    ]
