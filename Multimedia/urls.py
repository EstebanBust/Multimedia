"""
URL configuration for Multimedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from reproducir import views as reproducir
from descargas import views as descargas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videos/', reproducir.lista_videos, name='lista_videos'),
    path('download/', reproducir.download_video, name='download_video'),
    path('play_video/<path:video_path>/',reproducir.play_video, name='play_video'),
    path('search/', descargas.search_videos, name='search_videos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
