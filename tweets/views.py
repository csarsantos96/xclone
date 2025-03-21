from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Tweet
from .serializers import TweetSerializer
from .permissions import IsAuthorOrReadOnly

class TweetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class TweetListCreateAPIView(generics.ListCreateAPIView):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = TweetPagination

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)


class TweetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Tweet.objects.filter(author=self.request.user)


class TweetListAPIView(generics.ListAPIView):

    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TweetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Tweet.objects.filter(author=self.request.user)


class TweetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tweet.objects.filter(author=self.request.user)

class TweetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Tweet.objects.filter(author=self.request.user)