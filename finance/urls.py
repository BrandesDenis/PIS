from django.urls import path
from tasks import views

appname = 'finance'

urlpatterns = [
    path('types/new', views.TaskCreate.as_view(), name='task-create'),
    path('types/<int:pk>', views.TaskUpdate.as_view(), name='task-detail'),
    path('types/<int:pk>/delete', views.TaskDelete.as_view(), name='task-delete'),

    path('types/all', views.TaskList.as_view(), name='task-all'),
]
