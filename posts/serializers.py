from rest_framework import serializers
from posts.models import Post, Comment, Image, ImageModel

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
        fields = ('image_url','before_image', 'model', 'after_image',)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        exclude = ("post",)

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = ('user', 'title', 'image', 'content')

class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
        
    class Meta:
        model = Post
        fields = ("user", "title", "image", "content")

class PostListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()
    image = ImageSerializer()

    def get_user_id(self, obj):
        return obj.user.id

    def get_user(self, obj):
        return obj.user.username

    def get_likes(self, obj):
        return obj.likes.user

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_created_at(self, obj):
        return obj.created_at

    class Meta:
        model = Post
        fields = ("id", "title", "content", "image_id", "image", "created_at", "updated_at", "user", "likes_count", "comments", "likes", "user_id")

class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ("id", "user", 'likes', 'likes_count')

class BestPostSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()
    image = ImageSerializer()

    def get_user_id(self, obj):
        return obj.user.id

    def get_user(self, obj):
        return obj.user.username

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ("id", "user_id", "title", "content", "image", "user", "likes", "likes_count")

class ImageModelSerializer(serializers.ModelSerializer):
    model_path = serializers.SerializerMethodField()
    
    def get_model_path(self,obj):
        return obj.model_path

    class Meta:
        model = ImageModel
        fields = ('model_path',)

class ImageDetailSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self,obj):
        return obj.id
    class Meta:
        model = Image
        fields = ('__all__')