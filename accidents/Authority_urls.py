from django.urls import path
from django.contrib.auth import views as auth_views

from accidents.Authority_views import AddAccident, DeleteAccident, ViewAccident
from accidents.Authority_views import IndexView 


urlpatterns = [
    path('', IndexView.as_view()),
    path('AddAccident', AddAccident.as_view()),
    path('ViewAccident', ViewAccident.as_view(),name='view_accident'),
    path('DeleteAccident', DeleteAccident.as_view()),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ),
        name='logout'
    ),
]

def urls():
    return urlpatterns, 'Authority', 'Authority'