# blog/urls.py
from blog import views 
from django import forms
from .models import TravelPost
from django.urls import path
from .views import PostListView, PostDetailView, PostByCategoryView, PostByTagView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .views import PostUpdateView, PostDeleteView




urlpatterns = [
    # Ruta para la lista de publicaciones (la página principal)
    path('', PostListView.as_view(), name='post_list'), 
    
    # Ruta para los detalles de un post, usando el 'slug' como parámetro
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),  
    
    # Ruta para ver publicaciones por categoría
    path('category/<int:category_id>/', PostByCategoryView.as_view(), name='post_by_category'),  
    
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Ruta para ver publicaciones por etiqueta
    path('tag/<int:tag_id>/', PostByTagView.as_view(), name='post_by_tag'),
    path('', views.PostListView.as_view(), name='home'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<int:category_id>/', views.PostByCategoryView.as_view(), name='posts_by_category'),
    path('tag/<int:tag_id>/', views.PostByTagView.as_view(), name='posts_by_tag'),
    # Ejemplo de una ruta de registro de usuario (si tienes una vista de signup)
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('profile/', views.profile_view, name='profile'),  # Ruta para el perfil
    path('profile/update/', views.profile_update_view, name='profile_update'),

    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
