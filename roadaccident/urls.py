"""roadaccident URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from accidents.views import IndexView, RegisterView, LoginView, UserView, SignUp, get_heatmap_data,accident_map
from accidents import admin_urls,Authority_urls
from roadaccident import settings

urlpatterns = [
    path('', IndexView.as_view()),
    path('register', RegisterView.as_view(),name='register'),
    path('logins',LoginView.as_view(template_name='login.html'),name='logins'),
    path('admin/', admin_urls.urls()),
    path('Authority/', Authority_urls.urls()),
    path('SignUp', SignUp.as_view()),
    path("api/heatmap/", get_heatmap_data, name="heatmap_data"),
    path('map/', accident_map, name='accident_map'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)