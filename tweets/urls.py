from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TweetViewSet,
    TweetListCreateAPIView,
    TweetDetailAPIView,
    TweetListAPIView,
    TweetRetrieveUpdateDestroyAPIView,
    FeedTweetListAPIView
)
from django.conf import settings
from django.conf.urls.static import static

# Router para as rotas automáticas de CRUD
router = DefaultRouter()
router.register(r'tweets', TweetViewSet, basename='tweet')

urlpatterns = [
    path('', TweetListCreateAPIView.as_view(), name='tweet-list-create'),  # Corrigido para '/tweets/'
    path('<int:pk>/', TweetDetailAPIView.as_view(), name='tweet-detail'),  # Corrigido para '/tweets/<id>/'
    path('meus/', TweetListAPIView.as_view(), name='tweet-list-user'),  # Corrigido para '/tweets/meus/'
    path('meus/<int:pk>/', TweetRetrieveUpdateDestroyAPIView.as_view(), name='tweet-rud-user'),  # Corrigido para '/tweets/meus/<id>/'
    path('feed/', FeedTweetListAPIView.as_view(), name='feed-tweets'),  # Feed de tweets
    path('<int:pk>/like/', TweetViewSet.as_view({'post': 'like'}), name='tweet-like'),  # Corrigido para '/tweets/<id>/like/'
    path('<int:pk>/comment/', TweetViewSet.as_view({'post': 'comment'}), name='tweet-comment'),  # Corrigido para '/tweets/<id>/comment/'
    path('<int:pk>/retweet/', TweetViewSet.as_view({'post': 'retweet'}), name='tweet-retweet'),  # Corrigido para '/tweets/<id>/retweet/'
]

# Serve arquivos de mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
