from django.urls import path
from .views import HomePageView, PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('list/', PostListView.as_view(), name='post_list'),
    path('', HomePageView.as_view(), name='home')
]