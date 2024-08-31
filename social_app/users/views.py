from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import CustomUser, FriendRequest,CustomToken
from django.core.paginator import Paginator
from .serializers import UserSerializer, AuthTokenSerializer,FriendRequestSerializer
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle

class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def perform_create(self, serializer):
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        user = CustomUser.objects.create_user(email=email, password=password,first_name=first_name, last_name=last_name)
        user.save()


class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, created = CustomToken.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        search_keyword = self.request.query_params.get('search', '')
        users = CustomUser.objects.all()
        if '@' in search_keyword:
            users = users.filter(email__iexact=search_keyword)
        else:
            users = users.filter(
                Q(first_name__icontains=search_keyword) | Q(last_name__icontains=search_keyword)
            )
        paginator = Paginator(users, 10)
        page_number = self.request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return page_obj.object_list

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'

class FriendRequestView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request):
        sender = request.user
        receiver_email = request.data.get('receiver_email')
        receiver = CustomUser.objects.filter(email__iexact=receiver_email).first()
        if not receiver:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if sender == receiver:
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({'message': 'Friend request sent'}, status=status.HTTP_200_OK)

class FriendRequestResponseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = request.data.get('response')
        friend_request_id = request.data.get('friend_request_id')
        friend_request = FriendRequest.objects.filter(sender_id=friend_request_id, receiver=request.user).first()
        if not friend_request:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
        if response == 'accept':
            friend_request.delete()
            return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
        elif response == 'reject':
            friend_request.delete()
            return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid response'}, status=status.HTTP_400_BAD_REQUEST)

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = CustomUser.objects.filter(
            id__in=CustomUser.objects.filter(id__in=FriendRequest.objects.filter(
                receiver=user).values_list('sender', flat=True))
        )
        return friends

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user)
