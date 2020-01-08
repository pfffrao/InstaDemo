from django.urls import include, path
from Insta.views import HelloWorld, PostsView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', HelloWorld.as_view(), name='helloworld'),
    path('posts/', PostsView.as_view(), name='post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', PostCreateView.as_view(), name='make_post'),
    path('posts/update/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('posts/delete/<int:pk>', PostDeleteView.as_view(), name='delete_post')
]
