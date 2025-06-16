import uuid
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from . import models
from django.contrib.auth import login, logout
from . forms import ContactForm, LoginForm,RegisterForm,CommentForm,ArticleForm
from django.contrib import messages
from slugify import slugify
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def render_home_page(request):
    categories = [f'category-{i}' for i in range(1, 11)]
    questions = models.FAQ.objects.all()
    slides = models.Slider.objects.all()
    articles = models.Article.objects.all()

    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'categories': categories,
        'questions': questions,
        'slides': slides,
        'articles': articles,
    }
    return render(request, 'blog_app/index.html',context)

def render_about_page(request):
    return render(request, 'blog_app/about.html')

def render_contacts_page(request):
    return render(request, 'blog_app/contacts.html')

def render_faq_page(request):
    questions = models.FAQ.objects.all()
    context = {
        'questions': questions,
        
    }
    return render(request, 'blog_app/faq.html', context)

def render_articles_page(request):
    query_params = request.GET.get('category')
    page = request.GET.get('page')
    articles = models.Article.objects.all()

    if query_params:
        articles = articles.filter(category__slug=query_params)

    paginator = Paginator(articles, 3)
    
    articles = paginator.get_page(page)

    categories = models.Category.objects.all()
    context = {
        'articles': articles,
        'categories': categories,
        'slug': query_params
    }
    return render(request, 'blog_app/articles.html', context)

def render_register_page(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registation was successful')
            return redirect('login')
    else:
        form = RegisterForm()
        
    context = {
        'form': form
    }
    return render(request, 'blog_app/register.html',context)

def render_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'You have succesfully entered the account')
                return redirect('home')
            else:
                messages.error(request, 'The user not found')
        else:
            messages.error(request, 'Incorrect login or password')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html',context)

def render_article_detail_page(request, slug):
    article = models.Article.objects.get(slug=slug)
    comments = models.Comment.objects.filter(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            messages.success(request, 'Comment has succesfully been added')
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm

    if request.user.is_authenticated:
        is_viewed = models.ArticleCountView.objects.filter(
            article=article,
            user=request.user
        ).exists()

        if not is_viewed:
            obj = models.ArticleCountView.objects.create(
                article=article,
                user=request.user
            )
            article.views += 1
            article.save()

    try:
        article.likes
    except Exception as e:
        models.Like.objects.create(
            article=article
        )

    try:
        article.dislikes
    except Exception as e:
        models.Dislike.objects.create(article=article)

    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': comments.count()
    }
    return render(request, 'blog_app/article_detail.html',context)

def user_logout(request):
    logout(request)
    return redirect('home')

def article_create_page(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.slug = slugify(form.title)
            form.author = request.user
            form.save()

            obj = models.Article.objects.get(pk=form.pk)
            for item in request.FILES.getlist('gallery'):
                article = models.ArticleImage.objects.create(
                    article=obj,
                    photo=item
                )
                article.save()
            messages.success(request, 'The state has successfully been created')
            return redirect('article_detail', form.slug)
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = ArticleForm()

    context = {
        'form': form,
    }
    return render(request, 'blog_app/article_form.html',context)

class UpdateArticle(UpdateView):
    model = models.Article
    # success_url = '/articles/'
    form_class = ArticleForm
    template_name = 'blog_app/article_form.html'

class DeleteArticle(DeleteView):
    model = models.Article
    success_url = '/articles/'
    template_name = 'blog_app/article_confirm_delete.html'

def add_vote(request, article_id,action):
    article = models.Article.objects.get(pk=article_id)

    user = request.user
    if action == 'add_like':
        if user in article.likes.user.all():
            article.likes.user.remove(user.pk)
        else:
            article.likes.user.add(user.pk)
            article.dislikes.user.remove(user.pk)
    elif action == 'add_dislike':
        if user in article.dislikes.user.all():
            article.dislikes.user.remove(user.pk)
        else:
            article.dislikes.user.add(user.pk)
            article.likes.user.remove(user.pk)

    return redirect('article_detail',slug=article.slug)


def search(request):
    query = request.GET.get('q')
    articles = models.Article.objects.filter(title__iregex=query)
    context = {
        'articles': articles,
        'total_articles': articles.count(),
        'query': query
    }
    return render(request, 'blog_app/search.html', context)

@login_required(login_url='login')
def render_profile_page(request):
    user = request.user
    articles = models.Article.objects.filter(author=user)

    try:
        profile = user.user
        api_token = profile.api_token
    except models.UserProfile.DoesNotExist:
        api_token = None



    total_likes = 0
    total_dislikes = 0
    total_comments = 0
    total_views = 0


    for article in articles:
        total_comments += article.comments.all().count()
        total_views += article.articlecountview_set.all().count()

        likes = getattr(article, 'likes', None)
        if likes:
            total_likes += likes.user.all().count()

        dislikes = getattr(article, 'dislikes', None)
        if dislikes:
            total_dislikes += dislikes.user.all().count()

    context = {
        'total_articles': articles.count(),
        'total_comments': total_comments,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'articles': articles,
        'api_token': profile.api_token,
    }

    return render(request, 'blog_app/profile.html', context)

@login_required(login_url='login')
def generate_api_token(request):
    # Check if the user already has an API token
    profile, created = models.UserProfile.objects.get_or_create(user=request.user)

    if not created and profile.api_token:
        # If the user already has a token, return the existing token
        return JsonResponse({'token': profile.api_token})

    # Generate a new token if it doesn't exist
    new_token = str(uuid.uuid4())

    # Store the token in the user's profile
    profile.api_token = new_token
    profile.save()

    return JsonResponse({'token': new_token})

@login_required(login_url='login')
def render_api_page(request):
    user = request.user
    profile, created = models.UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'api_token': profile.api_token if profile.api_token else None,
    }
    
    return render(request, 'blog_app/api.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            send_mail(
            subject=f"New Contact Message: {subject}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL], 
            fail_silently=False,
            )

            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  
    else:
        form = ContactForm()
    
    return render(request, 'blog_app/contacts.html', {'form': form})
