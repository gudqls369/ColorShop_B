from django.urls import path 
from posts import views


urlpatterns = [
    path('', views.PostView.as_view(), name='post_view'),
    path('community/', views.CommunityView.as_view(), name='communit_view'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail_view'),
    path('<int:post_id>/comment/', views.CommentView.as_view(), name='comment_view'),
    path('<int:post_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'),
    path('<int:post_id>/like/', views.LikeView.as_view(), name='like_view'),
    path('image/', views.ImageView.as_view(), name='image_view'),
    path('choosemodel/<int:imagemodel_id>', views.ImageModelView().as_view(), name="imagemodel_view"),
]
