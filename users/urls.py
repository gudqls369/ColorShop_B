from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.UserView.as_view(), name='user_view'),
    path('mock/', views.MockView.as_view(), name='user_view'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
    path('changepassword/<int:user_id>/', views.ChangePasswordView.as_view(), name='change_password_view'),
]