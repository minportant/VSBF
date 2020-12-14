from django.urls import path, include
from django.views.generic import TemplateView


from . import views

app_name = 'finder'
urlpatterns = [
    path('', views.top_stories_index, name='top_stories_index'),
    path('profile/', TemplateView.as_view(template_name='finder/profile.html'), name='profile'),
    path('login/', TemplateView.as_view(template_name='finder/login.html'), name='login'),
    path('logout/', TemplateView.as_view(template_name='finder/logout.html'), name='logout'),
    path('profile/edit', views.profile, name='edit_profile'),
    path('search/', views.search, name='search'),
    path('top_stories/', views.top_stories_home, name='top_stories_home'),
    path('friendlist/', views.friendlist_home, name='friendlist_home'),
    path('sendRequest/<int:id>/', views.send_FriendRequest, name='send_request'),
    path('cancelRequest/<int:id>/', views.cancel_FriendRequest, name='cancel_request'),
    path('deleteRequest/<int:id>/', views.delete_FriendRequest, name='delete_request'),
    path('acceptRequest/<int:id>/', views.accept_FriendRequest, name='accept_request'),
    path('removeFriend/<int:id>/', views.remove_Friend, name='remove_friend'),
    path('groups/', views.groups, name='groups'),
    path('cancel_group_invite/<int:id>/', views.cancel_group_invite, name='cancel_group_invite'),
    path('invite_to_group/<int:id>/', views.invite_to_group, name='invite_to_group'),
    path('accept_group_request/<int:id>/', views.accept_GroupRequest, name='accept_group_request'),
    path('delete_group_request/<int:id>/', views.delete_GroupRequest, name='delete_group_request'),
    path('leave_group/', views.leave_group, name='leave_group'),
    path('create_group/', views.create_group, name='create_group'),
    path('<str:group_name>/', views.view_group, name="view_group")
]