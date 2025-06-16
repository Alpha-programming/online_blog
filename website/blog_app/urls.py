from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('about/', views.render_about_page,name='about'),
    path('contacts/', views.render_contacts_page,name='contacts'),
    path('faq/',views.render_faq_page, name='faq'),
    path('articles/',views.render_articles_page, name='articles'),
    path('register/', views.render_register_page, name='register'),
    path('login/', views.render_login_page, name='login'),
    path('articles/create/', views.article_create_page, name='create_article'),
    path('articles/<slug:slug>/',views.render_article_detail_page,name='article_detail'),
    path('profile/',views.render_profile_page,name='profile'),
    path('articles/<int:article_id>/<str:action>/',views.add_vote, name='add_vote'),
    path('articles/<slug:slug>/update/',views.UpdateArticle.as_view(),name='update'),
    path('articles/<slug:slug>/delete/',views.DeleteArticle.as_view(),name='delete'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name='search'),
    path('api/', views.render_api_page,name='api'),
    path('api/get-token/', views.generate_api_token, name='generate_api_token'),
    path('contact/', views.contact_view, name='contact'),
]
