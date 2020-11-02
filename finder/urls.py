from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'finder'
urlpatterns = [
    path('', TemplateView.as_view(template_name='finder/index.html'), name='index'),
    path('profile/', TemplateView.as_view(template_name='finder/profile.html'), name='profile'),
    path('profile/edit', views.profile, name='edit_profile'),
    path('search/', views.search, name='search'),
    path('friendlist/', views.friendlist_home, name='friendlist_home'),
    path('sendRequest/<int:id>/', views.send_FriendRequest, name='send_request'),
    path('cancelRequest/<int:id>/', views.cancel_FriendRequest, name='cancel_request'),
    path('deleteRequest/<int:id>/', views.delete_FriendRequest, name='delete_request'),
    path('acceptRequest/<int:id>/', views.accept_FriendRequest, name='accept_request'),
    path('removeFriend/<int:id>/', views.remove_Friend, name='remove_friend'),
]