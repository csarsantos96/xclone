from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Tweet, Like, Comment

class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    media = serializers.ImageField(required=False, allow_null=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'author',
            'content',
            'media',
            'created_at',
            'likes_count',
            'is_liked'
        ]
        read_only_fields = ['id', 'author', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.likes.filter(user=user).exists()

    def validate_media(self, value):
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError("O arquivo é muito grande; o tamanho máximo permitido é 2MB.")
        return value

    def create(self, validated_data):
        media_file = validated_data.pop('media', None)
        tweet = Tweet.objects.create(**validated_data)
        if media_file:
            tweet.media = media_file
            tweet.save()
        return tweet

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']
