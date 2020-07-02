from django.urls import path
from apps.tasks import views

appname = "tasks"

urlpatterns = [
    path("", views.TaskList.as_view(), name="task-all"),
    path("new", views.TaskCreate.as_view(), name="task-create"),
    path("<int:pk>", views.TaskUpdate.as_view(), name="task-detail"),
    path("<int:pk>/delete", views.TaskDelete.as_view(), name="task-delete"),
]
