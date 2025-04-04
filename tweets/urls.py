#tweets/urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TweetViewSet,
    TweetListCreateAPIView,
    TweetDetailAPIView,
    TweetListAPIView,
    TweetRetrieveUpdateDestroyAPIView,
    FeedTweetListAPIView,
    UserTweetsListAPIView ,
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'crud', TweetViewSet, basename='tweet')

urlpatterns = [
    path('', TweetListCreateAPIView.as_view(), name='tweet-list-create'),
    path('meus/', TweetListAPIView.as_view(), name='tweet-list-user'),
    path('meus/<int:pk>/', TweetRetrieveUpdateDestroyAPIView.as_view(), name='tweet-rud-user'),
    path('feed/', FeedTweetListAPIView.as_view(), name='feed-tweets'),
    path('<int:pk>/like/', TweetViewSet.as_view({'post': 'like'}), name='tweet-like'),
    path('<int:pk>/comment/', TweetViewSet.as_view({'post': 'comment'}), name='tweet-comment'),
    path('<int:pk>/retweet/', TweetViewSet.as_view({'post': 'retweet'}), name='tweet-retweet'),
    path('router/', include(router.urls)),  # Se quiser expor também as rotas automáticas

path('user/<str:username>/', UserTweetsListAPIView.as_view(), name='user-tweets-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
