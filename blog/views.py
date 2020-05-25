from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactUsForm, SignUpForm, CommentForm, CreatePostForm, UpdateAuthorForm, SearchForm
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Post, Author, Comment, Public_Post, Author_Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# Create your views here.

@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST.get('username')
            messages.success(request, f'{name} account created successfully.')
            return redirect('blog:login')
        else:
            messages.warning(request, f'Please Correct the errors!{str(form.errors)}')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'blog/register.html', context)


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username.upper()}! You are logged in.")
            return redirect('blog:dashboard')
        else:
            messages.warning(request, 'Username OR Password is incorrect!')
    context = {}
    return render(request, 'blog/new_login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Thanks for using our web services. You are logged out.")
    return redirect('blog:login')


def home(request):
    posts = Post.objects.all()
    slider_posts = posts.order_by('id')[0:6]
    picked_posts = posts.order_by('?')[0:5]
    recent_posts = posts.order_by('-published_date')[:5:]
    best_post = posts.get(title='The Wolf Story')
    # best_post = posts.order_by('?')[0:1]
    popular_posts = posts.order_by('-updated_date')[:5:]
    context = {
                'posts':posts,
                'slider_posts':slider_posts,
                'picked_posts':picked_posts,
                'recent_posts':recent_posts,
                'best_post':best_post,
                'popular_posts':popular_posts,

           }
    return render(request, 'blog/index.html', context)


@login_required(login_url='blog:login')
def dashboard_view(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    my_posts = posts.filter(creator=request.user.author)
    my_total_posts = my_posts.count()
    my_total_published_posts = my_posts.filter(status='P').count()
    my_total_draft_posts = my_posts.filter(status='D').count()
    # my_total_public_posts = my_posts.filter(privacy='Public').count()
    my_total_public_posts = my_posts.filter(status='P', privacy='Public').count()
    my_total_private_posts = my_posts.filter(privacy='Private').count()

    latest_posts = posts.order_by('-published_date')[:5:]
    top_posts = []
    for post in posts:
        com_count = post.comment_set.all().count()
        post_title = post.title
        t = (com_count, post_title)
        top_posts.append(t)
    top_posts.sort(reverse=True)
    # most = []
    most_commented = Post.objects.all().order_by('id')[0:2]
    # for post in most_commented:
    #     most = [(post.total_comments),(post.title)]
    # print(most)
    context = {
        'latest_posts': latest_posts,
        'comments': comments,
        'most_commented': most_commented,
        'my_total_posts': my_total_posts,
        'my_total_public_posts': my_total_public_posts,
        'my_total_private_posts': my_total_private_posts,
        'my_total_published_posts': my_total_published_posts,
        'my_total_draft_posts': my_total_draft_posts,
    }

    return render(request, 'blog/user-dashboard.html', context)


@login_required(login_url='blog:login')
def profile_view(request):
    author = Author.objects.get(slug=request.user)
    post_list = author.post_set.all()

    total_posts = post_list.count()
    recent_posts = post_list.order_by('-published_date')[:5:]

    context = {'post_list': post_list,
               'author': author,
               'total_posts': total_posts,
               'recent_posts': recent_posts,
               }
    return render(request, 'blog/user_profile.html', context)


@login_required(login_url='blog:login')
def settings_view(request):
    author = Author.objects.get(slug=request.user)
    context = {'author': author}
    return render(request, 'blog/settings.html', context)


class AuthorPostsList(LoginRequiredMixin, ListView):
    model = Author_Post
    paginate_by = 5
    template_name = "blog/my-posts-list.html"
    login_url = '/login/'
    redirect_field_name = 'blog:dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Author_Post.objects.all().filter(creator=self.request.user.author)
        print(Author_Post.objects.all().filter(creator=self.request.user.author).count())
        return context


class PostsList(ListView):
    model = Public_Post
    paginate_by = 10
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Public_Post.objects.all()
        context['popular_posts']  = Post.objects.order_by('-updated_date')[:5:]
        context['recent_posts']  = Post.objects.order_by('-published_date')[:5:]
        return context

def recent_posts(request):
    context = {
        "recent": 'recent',
        "object_list" : Post.objects.order_by('-published_date'),
        "popular_posts" : Post.objects.order_by('-updated_date')[:5:],
        "recent_posts" : Post.objects.order_by('-published_date'),
    }

    return render(request, 'blog/post_list.html',context)


def popular_posts(request):
    context = {
        "popular": 'popular',
        "object_list" : Post.objects.order_by('-updated_date')[:5:],
        "popular_posts" : Post.objects.order_by('-updated_date')[:5:],
        "recent_posts": Post.objects.order_by('-published_date'),
    }

    return render(request, 'blog/post_list.html',context)


def post_view(request, slug):
    popular_posts = Post.objects.all().order_by('-updated_date')[:5:]
    post = Post.objects.get(slug=slug)
    comments = post.comment_set.filter(active=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print("form is created!")
        if request.user.is_authenticated:
            print("user is authenticated!")
            if form.is_valid():
                print("form is valid!")
                new_comment = form.save(commit=False)
                new_comment.name = request.user.first_name or  request.user.username
                name = new_comment.name
                new_comment.email = request.user.email or  ''
                new_comment.post = post
                new_comment.comment_user = request.user.author
                new_comment.save()
                messages.success(request, f" Thanks for your interest {name}.")
                return redirect('blog:post', slug=post.slug)
        else:
            messages.warning(request, f"Please SignIn to  comment on posts! {form.errors}")
            return redirect("blog:login")

    context = {
        'post': post,
        'comments': comments,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='blog:login')
def create_post_view(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        print("validating of form starting")
        if form.is_valid:
            print("validated")
            post = form.save(commit=False)
            post.creator = Author.objects.get(name=request.user)
            post.save()
            return redirect('blog:my-posts')
        else:
            messages.warning(request, f"please correct the Errors!! {form.errors}")
            return redirect('blog:create-post')
    form = CreatePostForm()
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='blog:login')
def post_update_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        messages.error(request, "The requested post is not Found.")
        return redirect("blog:posts")
    if post.creator == request.user.author:
        if request.method == 'POST':
            form = CreatePostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, f"{post.title} post is updated successfully.")
                return redirect('blog:my-posts')
            # else:
            #     messages.error(request, f"Please correct the below errors! Post should contain unique name.")
        form = CreatePostForm(instance=post)
        context = {"form": form}
        return render(request, 'blog/post_update_form.html', context)
    else:
        messages.error(request, "You're are not allowed to view the requested page! You can update your Posts.")
        return redirect('blog:my-posts')


@login_required(login_url='blog:login')
def post_delete_view(request, slug):
    post = Post.objects.get(slug=slug)
    if post.creator == request.user.author or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('blog:my-posts')
        context = {'post': post}
        return render(request, 'blog/post_confirm_delete.html', context)
    else:
        messages.error(request, "You're are not allowed to delete Someone's Post! Here's your posts list.")
        return redirect('blog:my-posts')


class AuthorsList(ListView):
    model = Author
    paginate_by = 3


def author_view(request, slug):
    author = Author.objects.get(slug=slug)
    post_list = author.post_set.filter(~Q(status='D'), ~Q(privacy='Private'))
    recent_posts = post_list.order_by('-published_date')[:5:]
    total_posts = post_list.count()
    context = {'post_list': post_list,
               'author': author,
               'total_posts': total_posts,
               'recent_posts': recent_posts,
               }
    return render(request, 'blog/author_detail.html', context)


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Post.objects.filter(Q(title__icontains=query)
                                        | Q(category__icontains=query)
                                        | Q(content__icontains=query))
            if posts:
                posts = posts
                context = {
                    'query': query,
                    'object_list': posts,
                    'popular_posts': Post.objects.all().order_by('-updated_date')[:5:]
                }
                return render(request, 'blog/post_list.html', context)
            else:
                messages.warning(request, f'No Post or Author Found with the given keywords {query}')
                return redirect('/')

        return HttpResponseRedirect('/')


@login_required(login_url='blog:login')
def author_update_view(request, slug):
    if slug == request.user.author.slug:
        author = Author.objects.get(slug=slug)
    else:
        messages.error(request, "You're are not allowed to view the requested page! You can update your profile.")
        author = Author.objects.get(slug=request.user.author.slug)

    if request.method == "POST":
        form = form = UpdateAuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('blog:user-profile')
        else:
            messages.error(request, "plaease correct the errors")

    form = UpdateAuthorForm(instance=author)
    context = {"form": form}
    return render(request, 'blog/author_form.html', context)

# @login_required(login_url='blog:login')
def contact_mail(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            mail = request.POST.get('email')
            sub = request.POST.get('subject')
            meassage = request.POST.get('body')

            email = EmailMessage(
                'Hello! You got a mail from ' + "mail",
                "Name : " + str(name) + '\n'
                                        f"Email : {str(mail)} \n"
                                        f"Subject : {str(sub)} \n"
                                        f"Meassage : {str(meassage)} \n",
                settings.EMAIL_HOST_USER,  # 'from@example.com',
                ['nagaraj015973@gmail.com', 'love.haters.fully@gmail.com'],  # to@example.com',
            )
            email.send(fail_silently=False)
            form.save()
            messages.success(request, f" Thanks for Contacting Us \' {name} \'. We'll contact you by your requested mail \' {mail} \'")
            return redirect('blog:home')

    return render(request, 'blog/contactus.html')
