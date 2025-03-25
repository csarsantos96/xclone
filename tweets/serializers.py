from rest_framework import serializers
from .models import Tweet
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
    author = serializers.StringRelatedField(read_only=True)  # Exibe o username, por exemplo.

    class Meta:
        model = Tweet
        fields = ['id', 'author', 'content', 'created_at', 'media']
        read_only_fields = ['id', 'author', 'created_at']


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
