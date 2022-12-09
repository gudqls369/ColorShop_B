from django.contrib import admin
from posts.models import Post, Comment, Image, ImageModel

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(ImageModel)
