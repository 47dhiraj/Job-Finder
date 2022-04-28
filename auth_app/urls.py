from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('register/', views.RegistrationView.as_view(), name='register'),

    path('login/', views.LoginView.as_view(), name='login'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('activate/<slug:uidb64>/<slug:token>/', views.ActivateAccountView.as_view(), name='activate'),

    path('request_reset_email/', views.RequestResetEmailView.as_view(), name='reset_email'),

    path('set_new_password/<slug:uidb64>/<slug:token>/', views.SetNewPasswordView.as_view(), name='set_new_password'),

    path('accounts/', include('allauth.urls')),
    
]


