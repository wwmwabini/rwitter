from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path("", views.home, name="tweets-home"),
    path("search/", views.searchresults, name="tweets-searchresults"),
    path("feedback/", views.feedback, name="tweets-feedback"),
    path("post/new", PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]