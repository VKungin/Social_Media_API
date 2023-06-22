from django.contrib import admin

from social.models import Profile, Hashtag, Post

admin.site.register(Profile)
admin.site.register(Hashtag)
admin.site.register(Post)
