from django.urls import path
from django.contrib.auth import views as auth_views
from accidents.admin_views import ApproveView, IndexView, NewAuthority, RejectView,View_Authority
from accidents.models import Authority

urlpatterns=[
    path('', IndexView.as_view()),
    path('NewAuthority', NewAuthority.as_view()),
    path('View_Authority',View_Authority.as_view()),
    path('ApproveView', ApproveView.as_view()),
    path('RejectView', RejectView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ),
        name='logout'
    ),
]

def urls():
    return urlpatterns, 'admin', 'admin'
