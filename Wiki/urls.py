"""
URL configuration for Wiki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path , include
from WikiPage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.global_search, name='global_search'),
    path('crews/', views.crew_list, name='crews'), 
    path('characters/', views.character_list, name='characters'), 
    path('character/<int:id>/', views.character, name='character'),
    path('fruits/', views.fruits_list, name='fruits'),  
    path('sagas/', views.saga_list, name='sagas'),
    path('arcs/', views.saga_list, name='arcs'),
    path('chapters/', views.chapter_list, name='chapters'),
    
]
