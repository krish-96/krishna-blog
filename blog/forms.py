from django import forms
from .models import ContactUs, Comment, Post, Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class CreatePostForm(forms.ModelForm):
    title = forms.CharField( label='Post Title')
    # slug = forms.CharField( label='Post Slug')
    class Meta:
        model = Post
        fields = ['title', 'post_pic', 'category','tags', 'content',   'status' , 'privacy']
        widgets = {

            'content': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Write about your Post  here.','cols': 80, 'rows':15}),
            'status': forms.RadioSelect(attrs={'class': 'checkbox','type':'radio' }),
            'privacy': forms.RadioSelect(attrs={'class': 'checkbox','type':'radio' }),
            # 'tags': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox','type':'checkbox' }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'body']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"

class UpdateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name',  'phone_no', 'email', 'address',  'photo' , 'about']

class SearchForm(forms.Form):
    query = forms.CharField()