from django.urls import path
from apps.finance import views

appname = "finance"

urlpatterns = [
    path("", views.IndexView.as_view(), name="finance-index"),
    path("objects/new", views.FinanceObjectCreate.as_view(), name="objects-create"),
    path(
        "objects/<int:pk>", views.FinanceObjectUpdate.as_view(), name="objects-detail"
    ),
    path(
        "objects/<int:pk>/delete",
        views.FinanceObjectDelete.as_view(),
        name="objects-delete",
    ),
    path("objects/all", views.FinanceObjectList.as_view(), name="objects-all"),

    path("day_reports/new", views.DayReportView.as_view(), name="day_reports-create"),
    path(
        "day_reports/<int:pk>", views.DayReportView.as_view(), name="day_reports-detail"
    ),
    path(
        "day_reports/<int:pk>/delete",
        views.DayReportDelete.as_view(),
        name="day_reports-delete",
    ),
    path("day_reports/all", views.DayReportList.as_view(), name="day_reports-all"),

    path("budgets/new", views.BudgetView.as_view(), name="budgets-create"),
    path(
        "budgets/<int:pk>", views.BudgetView.as_view(), name="budgets-detail"
    ),
    path(
        "budgets/<int:pk>/delete",
        views.BudgetDelete.as_view(),
        name="budgets-delete",
    ),
    path("budgets/all", views.BudgetList.as_view(), name="budgets-all"),

    path("periodic_reports/new", views.PeriodicReportView.as_view(),
         name="periodic_reports-create"),
    path(
        "periodic_reports/<int:pk>", views.PeriodicReportView.as_view(),
        name="periodic_reports-detail"
    ),
    path(
        "periodic_reports/<int:pk>/delete",
        views.PeriodicReportDelete.as_view(),
        name="periodic_reports-delete",
    ),
    path("periodic_reports/all", views.PeriodicReportList.as_view(),
         name="periodic_reports-all"),

    path("report", views.ReportView.as_view(), name="finance-report"),
    path("fin_object_detalization_report/<int:pk>",
         views.FinObjectDetalizationReportView.as_view(),
         name="finance-object-detalization"),
]
