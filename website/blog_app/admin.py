from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['pk','title','description','image']
    list_display_links = ['pk','title']

@admin.register(models.FAQ)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['pk','question', 'answer']
    list_display_links = ['pk', 'question']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['pk', 'name']
    list_filter = ['created_at']
    search_fields = ['name']

class ArticleImageInline(admin.TabularInline):
    model = models.ArticleImage
    extra = 1

class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 1

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views']
    inlines = [ArticleImageInline,CommentInline]

admin.site.register(models.Comment)
