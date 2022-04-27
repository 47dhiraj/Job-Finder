from django.urls import path

from app.views import home_views as views



urlpatterns = [

    path('', views.LandingView.as_view(), name="land"),

    

]