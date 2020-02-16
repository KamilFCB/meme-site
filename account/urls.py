from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('manage/', views.manage_view, name='manage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('login_validate', views.login_validate, name='login_validate'),
    path('register_validate', views.register_validate, name='register_validate')
]
