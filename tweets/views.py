from rest_framework import generics, permissions, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


from .permissions import IsAuthorOrReadOnly
from .models import Tweet, Like, Comment, Repost
from .serializers import TweetSerializer, CommentSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # ✅ agora sim, completo

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        tweet = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(user=user, tweet=tweet)
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        tweet = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Conteúdo obrigatório'}, status=400)
        comment = Comment.objects.create(user=request.user, tweet=tweet, content=content)
        return Response({'status': 'comentado', 'comment_id': comment.id})

    @action(detail=True, methods=['post'])
    def retweet(self, request, pk=None):
        tweet = self.get_object()
        new_tweet = Tweet.objects.create(
            author=request.user,
            content=f"RT: {tweet.content}",
            media=tweet.media
        )
        Repost.objects.create(user=request.user, original_tweet=tweet)
        serializer = self.get_serializer(new_tweet)
        return Response(serializer.data, status=201)

class TweetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class TweetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TweetPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def perform_create(self, serializer):
        print("👤 Request.user:", self.request.user)
        print("🔒 Is authenticated:", self.request.user.is_authenticated)
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
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Tweet.objects.filter(author=self.request.user)

class FeedTweetListAPIView(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list('id', flat=True)
        return Tweet.objects.filter(
            Q(author__id__in=following_ids) | Q(author=user)
        ).order_by('-created_at')

class UserTweetsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Tweet.objects.filter(author__username=username).order_by('-created_at')
