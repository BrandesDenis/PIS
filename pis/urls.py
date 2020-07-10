from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.main_page.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("finance/", include("apps.finance.urls")),
    path("thoughts/", include("apps.thoughts.urls")),
    path("reading/", include("apps.reading.urls")),
]
