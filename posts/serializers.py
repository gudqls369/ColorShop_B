from rest_framework import serializers
from posts.models import Post, Comment


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
        fields = ("pk", "title", "image", "updated_at", "user", "likes", "comments", "likes_count", "comments_count")  # 추가
