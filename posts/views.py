from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db.models.query_utils import Q
from posts.models import Post, Comment
<<<<<<< HEAD
from posts.serializers import PostSerializer, PostListSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer, PostLikeSerializer
=======
from posts.serializers import PostSerializer, PostListSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
>>>>>>> eadcd232bc60fc4c2554d36f9e5d06b727fa1bd7


class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True) # 복수
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'message':'로그인이 필요합니다'}, 401)
        serializer = PostCreateSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(user=request.user)
            # return Response(serializer.data)
            return Response({'message':'작성 완료'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedView(APIView): # 로그인된 사람 permissions
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = Q()
        for user in request.user.followings.all(): # 내가 팔로우하는 모든 유저
            q.add(Q(user=user),q.OR)
        feeds = Post.objects.filter(q) # follow하는 사람의 글을 모두 가져오기
        serializer = PostListSerializer(feeds, many=True) # 시리얼라이저 가져오기
        return Response(serializer.data)


class PostDetailView(APIView):
    def get(self, request, post_id): 
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer = PostCreateSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    # 삭제
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            post.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
<<<<<<< HEAD
        comments = post.comment_set.all() 
=======
        comments = post.comments.all() 
>>>>>>> eadcd232bc60fc4c2554d36f9e5d06b727fa1bd7
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id) 
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response("unlike", status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response("like", status=status.HTTP_200_OK)