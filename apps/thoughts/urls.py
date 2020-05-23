from django.urls import path
from pis_thoughts.apps.thoughts import views


urlpatterns = [
    path("", views.ThoughtListView.as_view()),
    path("new", views.ThoughtListView.as_view()),
    path("<int:thought_id>", views.ThoughtView.as_view()),
]
