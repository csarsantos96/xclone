from django.urls import path
from .views import (
    TweetListCreateAPIView,
    TweetDetailAPIView,
    TweetListAPIView,
    TweetRetrieveUpdateDestroyAPIView,
FeedTweetListAPIView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TweetListCreateAPIView.as_view(), name='tweet-list-create'),
    path('<int:pk>/', TweetDetailAPIView.as_view(), name='tweet-detail'),
    path('meus/', TweetListAPIView.as_view(), name='tweet-list-user'),
    path('meus/<int:pk>/', TweetRetrieveUpdateDestroyAPIView.as_view(), name='tweet-rud-user'),

path('feed/', FeedTweetListAPIView.as_view(), name='feed-tweets'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
