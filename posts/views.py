from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response
from posts.models import Post, Comment, Image, ImageModel
from posts.serializers import (BestPostSerializer, PostSerializer, PostListSerializer, 
                                PostCreateSerializer, PostLikeSerializer, 
                                CommentSerializer, CommentCreateSerializer, 
                                ImageSerializer, ImageCreateSerializer, 
                                ImageModelSerializer, ImageDetailSerializer)
from AutoPainter.app2 import trans1, trans2, sketchify2

class PostView(APIView):
    def get(self, request):

        posts = Post.objects.all().order_by("-likes")
        posts=set(posts)
        posts=list(posts)
        posts= posts[:8]
        serializer = BestPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'message':'로그인이 필요합니다'}, 401)
        serializer = PostCreateSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    def get(self, request, post_id): 
        post = get_object_or_404(Post, id=post_id)
        serializer = PostListSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

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
        comments = post.comments.all() 
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
            return Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response("좋아요를 했습니다.", status=status.HTTP_200_OK)

class ImageView(APIView):
    def get(self, request):
        image = Image.objects.all()
        serializer = ImageSerializer(image, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ImageTrans1View(APIView):
    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save(user=request.user)
            url = image.image_url
            result = trans1(url)
            filename = str(result)[str(result).index('\\')+1:]
            
            bf_img = 'before_image/' + filename
            af_img = 'after_image/' + filename
            
            serializer.save(before_image=bf_img, after_image=af_img)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ImageTrans2View(APIView):
    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save(user=request.user)
            url = image.image_url
            result = trans2(url)
            filename = str(result)[str(result).index('\\')+1:]
            
            bf_img = 'before_image/' + filename
            af_img = 'after_image/' + filename
            
            serializer.save(before_image=bf_img, after_image=af_img)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class ImageSketchifyView(APIView):
    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save(user=request.user)
            url = image.image_url
            result = sketchify2(url)
            filename = str(result)[str(result).index('\\')+1:]
            
            bf_img = 'before_image/' + filename
            af_img = 'after_image/' + filename
            
            serializer.save(before_image=bf_img, after_image=af_img)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CommunityView(APIView):
    def get(self, request):
            posts = Post.objects.all()
            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ImageModelView(APIView):
    def get(self, request, imagemodel_id):
        model = get_object_or_404(ImageModel, id=imagemodel_id)
        serializer = ImageModelSerializer(model)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ImageDetailView(APIView):
    def get(self, request, image_id):
        aimage = get_object_or_404(Image, id=image_id)
        serializer = ImageDetailSerializer(aimage)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        if request.user == image.user:
            image.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class PostSearchView(APIView):
    def get(self, request, **kwargs):
        searchSelect = request.GET.get('searchSelect')
        searchText = request.GET.get('searchText')

        if searchText == None:
            query_set = Post.objects.all()
        else:
            if searchSelect == '전체':
                query_set = Post.objects.filter(Q(title__icontains=searchText) |
                                                Q(content__icontains=searchText) |
                                                Q(user__username__icontains=searchText)).distinct() 
            elif searchSelect == '제목':
                query_set = Post.objects.filter(Q(title__icontains=searchText)).distinct() 
            elif searchSelect == '내용':
                query_set = Post.objects.filter(Q(content__icontains=searchText)).distinct() 
            elif searchSelect == '작성자':
                query_set = Post.objects.filter(Q(user__username__icontains=searchText)).distinct()

        serializer = PostListSerializer(query_set, many=True)
        return Response(serializer.data)