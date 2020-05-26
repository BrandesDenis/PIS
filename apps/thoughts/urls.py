from django.urls import path
from apps.thoughts import views


urlpatterns = [
    path("", views.ThoughtListView.as_view(), name="thoughts-list"),
    path("new", views.ThoughtView.as_view(), name="thoughts-new"),
    path("<int:pk>", views.ThoughtView.as_view(), name="thoughts-detail"),
    path("<int:pk>/delete", views.ThoughtDeleteView.as_view(), name="thoughts-delete"),
]
