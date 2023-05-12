from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet,LikePostView,CommentListCreateView,SimilarPostsView,PostSuggestionsView
router = DefaultRouter()
router.register('',PostViewSet,'posts')

urlpatterns = [
    path('suggestions/',PostSuggestionsView.as_view(),name='suggested_posts'),
    path('<int:post_id>/like/',LikePostView.as_view(),name='like_post'),
    path('<int:post_id>/comments/',CommentListCreateView.as_view(),name='comment_post'),
    # path('<int:post_id>/comments/',CommentListCreateView.as_view()),
    path('<int:post_id>/similar_posts/',SimilarPostsView.as_view(),name='get_similar_posts'),
    path('',include(router.urls)),
]

