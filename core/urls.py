from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-options/', views.register_options, name='register_options'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_page, name='profile'),
    path('security/', views.security_page, name='security'),
    path('resume/create/', views.resume_create, name='resume_create'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('my-resumes/', views.my_resumes, name='my_resumes'),
    path('search/', views.search_specialists, name='search_specialists'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('favorite/<int:resume_id>/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('notifications/', views.notifications_page, name='notifications'),
]
