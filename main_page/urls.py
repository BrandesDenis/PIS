from django.urls import path
from main_page import views

appname = 'main_page'

urlpatterns = [
    path('', views.IndexView.as_view(), name='main-index'),
]
