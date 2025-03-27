

# Register your models here.
# tweets/admin.py
from django.contrib import admin
from .models import Tweet, TweetMedia

admin.site.register(Tweet)
admin.site.register(TweetMedia)
