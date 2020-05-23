from django.urls import path, include


urlpatterns = [
    path("", include("apps.main_page.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("finance/", include("apps.finance.urls")),
]
