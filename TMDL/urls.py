"""
URL configuration for TMDL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import index, classic_extendedlist, classic_legacylist, classic_stat_viewer, platformer_mainlist, platformer_stat_viewer, guidelines

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('classic_extendedlist/', classic_extendedlist, name='classic_extendedlist'),
    path('classic_legacylist/', classic_legacylist, name='classic_legacylist'),
    path('classic_stat_viewer/', classic_stat_viewer, name='classic_stat_viewer'),
    path('platformer_mainlist/', platformer_mainlist, name='platformer_mainlist'),
    path('platformer_stat_viewer/', platformer_stat_viewer, name='platformer_stat_viewer'),
    path('guidelines/', guidelines, name='guidelines'),
]