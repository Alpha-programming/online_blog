from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='slider/')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = 'Question and answer'
        verbose_name_plural = 'Questions and answers'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(help_text='This field will be automatically filled in.')
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Article(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    full_description = models.TextField(null=True, blank=True)
    preview = models.ImageField(upload_to='articles/previews', null=True, blank=True)
    views = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug':self.slug})


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

class ArticleImage(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='images')
    photo = models.ImageField(upload_to='articles/gallery/')

    class Meta:
        verbose_name = 'Gallery of a state'
        verbose_name_plural = 'Gallery of state'

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.article}'
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    

class ArticleCountView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE,related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE,related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    api_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"