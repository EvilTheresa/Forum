from django.urls import path
from django.views.generic import RedirectView

from webapp.views.comments import CreateReplyView, UpdateReplyView, DeleteReplyView
from webapp.views.topics import TopicListView, TopicCreateView, TopicDetailView, TopicUpdateView, TopicDeleteView

app_name = 'webapp'

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topics'),
    path('', RedirectView.as_view(pattern_name='webapp:topics')),
    path('create/', TopicCreateView.as_view(), name='create_topic'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:pk>/update/', TopicUpdateView.as_view(), name='update_topic'),
    path('topic/<int:pk>/delete/', TopicDeleteView.as_view(), name='delete_topic'),
    path('topic/<int:pk>/reply/create/', CreateReplyView.as_view(), name='create_comment'),
    path('reply/<int:pk>/update/', UpdateReplyView.as_view(), name='update_comment'),
    path('reply/<int:pk>/delete/', DeleteReplyView.as_view(), name='delete_comment'),
]