from django.urls import path

from app.views import home_views as views



urlpatterns = [

    path('', views.LandingView.as_view(), name="land"),

    path('contact/', views.ContactView.as_view(), name="contact"),

    path('about/', views.AboutView.as_view(), name="about"),


]
