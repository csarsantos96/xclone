#root/urls
"""
URL configuration for xclone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from frontend.views import FrontendAppView
from tweets.views import FeedTweetListAPIView, TweetDetailAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Rotas da API
    path("api/accounts/", include("accounts.urls")),
    path("api/tweets/", include("tweets.urls")),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Rotas adicionais da API
    path("api/tweets/feed/", FeedTweetListAPIView.as_view(), name="feed-tweets"),
    path("api/tweets/<int:pk>/", TweetDetailAPIView.as_view(), name="tweet-detail"),

    # React fallback – serve index.html pra qualquer rota que não seja /api/ ou /admin/
    re_path(r"^(?!api/|admin/).*", FrontendAppView.as_view(), name="frontend"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
