from django.urls import path
from .views import PostListView, PostDetailView,\
    PostCreateView, PostUpdateView, PostDeleteView,\
    MyPostView

urlpatterns = [
    path('post1', PostListView.as_view(), name='post1'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/update', PostUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete', PostDeleteView.as_view(), name='delete'),
    path('dashboard/myposts/', MyPostView.as_view(), name='my_posts'),
]
