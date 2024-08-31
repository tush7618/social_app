from django.urls import path
from .views import (
    UserSignupView, UserLoginView, UserSearchView,
    FriendRequestView, FriendRequestResponseView,
    ListFriendsView, ListPendingFriendRequestsView
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request-response/', FriendRequestResponseView.as_view(), name='friend-request-response'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('pending-requests/', ListPendingFriendRequestsView.as_view(), name='pending-requests'),
]

