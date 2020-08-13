from django.urls import path
from apps.thoughts import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="thoughts-index"),

    path("topics", views.TopicList.as_view(), name="topics-list"),
    path("topics/new", views.TopicCreate.as_view(), name="topics-new"),
    path("topics/<int:pk>", views.TopicUpdate.as_view(), name="topics-detail"),
    path("topics/<int:pk>/delete", views.TopicDelete.as_view(), name="topics-delete"),

    path("list", views.ThoughtListView.as_view(), name="thoughts-list"),
    path("new", views.ThoughtView.as_view(), name="thoughts-new"),
    path("<int:pk>", views.ThoughtView.as_view(), name="thoughts-detail"),
    path("<int:pk>/delete", views.ThoughtDeleteView.as_view(), name="thoughts-delete"),
]
