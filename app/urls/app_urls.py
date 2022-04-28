from django.urls import path

from app.views import home_views as views



urlpatterns = [

    path('home/', views.HomeView.as_view(), name="home"),

    
]
