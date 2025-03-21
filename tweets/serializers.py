from rest_framework import serializers
from .models import Tweet
from .models import Tweet, TweetMedia

class TweetSerializer(serializers.ModelSerializer):
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