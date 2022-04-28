from django.contrib import admin
from django.urls import path, include

from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('app.urls.landing_urls')),

    path('', include('app.urls.app_urls')),

    path('', include('auth_app.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
