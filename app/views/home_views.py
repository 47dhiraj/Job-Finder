from django.shortcuts import render, redirect
from django.views.generic import View


class LandingView(View):
    def get(self, request):
        return render(request, 'landing/index.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'landing/contact.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'landing/about.html')


class HomeView(View):
    def get(self, request):
        return render(request, 'app/index.html')

