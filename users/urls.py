from django.urls import path,include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from . import views


router = routers.DefaultRouter()

router.register('',views.UserApiViewSet,basename='users')

urlpatterns = [
    path('search/',views.UserSearchView.as_view(),name='user_search'),
    path('login/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('suggestions/',views.UserSuggestionsView.as_view(),name='suggestions_to_follow'),
    path('login/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/posts/',views.UserPostsView.as_view(),name='get_user_posts'),
    path('<int:user_id>/<str:action>/',views.UserFollowView.as_view(),name='follow_or_unfollow_user'),
    path('',include(router.urls)),
]