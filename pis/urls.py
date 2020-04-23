from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('main_page.urls')),
    path('tasks/', include('tasks.urls')),
    path('finance/', include('finance.urls')),
]
