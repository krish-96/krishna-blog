from django.contrib import admin
from .models import ContactUs, Author, Post, Comment,  NewsLetter
from import_export.admin import ImportExportModelAdmin

@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    list_display = ['name', 'dob', 'phone_no', 'email', 'address', 'slug', 'about', 'photo', 'joined_date']



@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    list_display = ['title', 'creator', 'post_pic', 'category', 'slug', 'privacy', 'status', 'published_date']


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ['post','comment_user', 'name', 'email', 'body', 'created_date', 'updated_date', 'active']

@admin.register(ContactUs)
class ContactUsAdmin(ImportExportModelAdmin):
    list_display = ['name', 'email', 'subject', 'body']

admin.site.register(NewsLetter)