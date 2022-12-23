from django.urls import path 
from posts import views

urlpatterns = [
    path('', views.PostView.as_view(), name='post_view'),
    path('community/', views.CommunityView.as_view(), name='communit_view'),
    path('search/', views.PostSearchView.as_view(), name='post_list_view'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail_view'),
    path('<int:post_id>/comment/', views.CommentView.as_view(), name='comment_view'),
    path('<int:post_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'),
    path('<int:post_id>/like/', views.LikeView.as_view(), name='like_view'),
    path('image/', views.ImageView.as_view(), name='image_view'),
    path('image/<int:image_id>/', views.ImageDetailView.as_view(), name='image_detail_view'),
    path('choosemodel/<int:imagemodel_id>/', views.ImageModelView().as_view(), name="imagemodel_view"),
    path('sketchify/', views.ImageSketchifyView().as_view(), name="imagesketchify_view"),
    path('trans1/', views.ImageTrans1View().as_view(), name="imagetrans1_view"),
    path('trans2/', views.ImageTrans2View().as_view(), name="imagetrans2_view"),
]
