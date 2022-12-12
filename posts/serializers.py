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
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
        
    class Meta:
        model = Post
        fields = ("user", "title", "image", "content")  # 검증에 필요한 부분


class PostListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.user.id

    def get_user(self, obj):  # obj: 해당 post
        return obj.user.username

    def get_likes(self, obj):
        return obj.likes.user

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ("id", "title", "content", "image_id", "created_at", "updated_at", "user", "likes_count", "comments", "likes", "user_id")  # 추가


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

class BestPostSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

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