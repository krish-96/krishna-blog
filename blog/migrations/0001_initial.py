# Generated by Django 3.0.5 on 2020-04-18 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('phone_no', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, max_length=1000, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='author_img/')),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.OneToOneField(max_length=64, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=264)),
                ('body', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, max_length=10000, null=True)),
                ('post_pic', models.ImageField(blank=True, null=True, upload_to='post_img/')),
                ('slug', models.SlugField(default='hello', max_length=100, unique='True')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('D', 'draft'), ('P', 'published')], default='D', max_length=2)),
                ('privacy', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author')),
            ],
            options={
                'unique_together': {('title', 'slug')},
            },
        ),
    ]
