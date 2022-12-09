from rest_framework import serializers
from posts.models import Post, Comment, Image, ImageModel


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ("post",) # 1개만 제외할 때는 exclude를 쓰기도 한다.


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True)

    def get_user(self, obj):
        return obj.user.username # 유저 이메일이 돌아가게 되어 있다.

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "image", "content")  # 검증에 필요한 부분


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_user(self, obj):  # obj: 해당 post
        return obj.user.username

    def get_likes(self, obj):
        return obj.likes.user

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.user

    def get_comments_count(self, obj):
        return obj.comments.count() # 변경 주의

    class Meta:
        model = Post
        fields = ("id", "title", "image", "updated_at", "user", "likes_count", "comments_count", "comments", "likes")  # 추가


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ("id", "user", "likes_count", 'likes')

class ImageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username
    class Meta:
        model = Image
        fields = '__all__'

class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('before_image', 'model', 'after_image',)
        
class ImageModelSerializer(serializers.ModelSerializer):
    model_path = serializers.SerializerMethodField()
    
    def get_model_path(self,obj):
        return obj.model_path
    class Meta:
        model = ImageModel
        fields = ('model_path',)