from django.shortcuts import render, redirect
from django.views.generic import View


class LandingView(View):
    def get(self, request):
        return render(request, 'landing/index.html')



