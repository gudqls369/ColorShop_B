from django.contrib import admin
from posts.models import Post, Comment, Image


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)