from re import template
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
#from django.conf.urls import patterns,url
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
     


    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='authentication/admin/registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='authentication/admin/registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/admin/registration/password_reset_done.html'),
     name='password_reset_done'),

    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='authentication/admin/registration/password_reset_confirm'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/admin/registration/password_reset_confirm.html"), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html')),
   path('password_reset/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/admin/registration/password_reset.html'),
        name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/admin/registration/password_reset_complete.html'),
     name='password_reset_complete'),

    #path('accounts/', include('django.contrib.auth.urls')), # Admin access
]
