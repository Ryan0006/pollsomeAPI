from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('signup/', views.CreateAccount.as_view(), name="signup"),
    path('user/<int:user_id>', views.UserDetail.as_view(), name='user'),
    path('account/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('account/token/refresh/',
         jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
