from django.urls import path
from tasks import views

appname = 'tasks'

urlpatterns = [
    path('new', views.TaskCreate.as_view(), name='task-create'),
    path('<int:pk>', views.TaskUpdate.as_view(), name='task-detail'),
    path('<int:pk>/delete', views.TaskDelete.as_view(), name='task-delete'),

    path('all', views.TaskList.as_view(), name='task-all'),
]
