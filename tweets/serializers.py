from rest_framework import serializers

from .models import Tweet, TweetMedia
from .models import Like, Repost, Comment

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

class TweetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetMedia
        fields = ['id', 'file', 'media_type']

    def validate_file(self, value):
        max_size = 2 * 1024 * 1024  # 2 MB em bytes
        if value.size > max_size:
            raise serializers.ValidationError("O arquivo é muito grande; o tamanho máximo permitido é 2MB.")
        return value

    def create(self, validated_data):
        media_data = validated_data.pop('media', [])
        tweet = Tweet.objects.create(**validated_data)
        for media_item in media_data:
            TweetMedia.objects.create(tweet=tweet, **media_item)
        return tweet


class TweetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    media = serializers.ImageField(required=False, allow_null=True)  # ou FileField, dependendo do seu uso
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'author',
            'content',
            'media',          # Adicione este campo
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

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']