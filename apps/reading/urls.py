from django.urls import path
from apps.reading import views

appname = "main_page"

urlpatterns = [
    path("", views.ReadingList.as_view(), name="reading-list"),
    path("new", views.ReadingCreate.as_view(), name="reading-create"),
    path("<int:pk>", views.ReadingUpdate.as_view(), name="reading-detail"),
    path("<int:pk>/delete", views.ReadingDelete.as_view(), name="reading-delete"),
    path("<int:pk>/files", views.ReadingFiles.as_view(), name="reading-files"),
]
