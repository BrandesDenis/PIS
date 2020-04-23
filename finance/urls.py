from django.urls import path
from finance import views

appname = 'finance'

urlpatterns = [
    path('', views.IndexView.as_view(), name='finance-index'),

    path('types/new', views.FinanceObjectTypeCreate.as_view(), name='types-create'),
    path('types/<int:pk>', views.FinanceObjectTypeUpdate.as_view(), name='types-detail'),
    path('types/<int:pk>/delete', views.FinanceObjectTypeDelete.as_view(), name='types-delete'),
    path('types/all', views.FinanceObjectTypeList.as_view(), name='types-all'),

    path('objects/new', views.FinanceObjectCreate.as_view(), name='objects-create'),
    path('objects/<int:pk>', views.FinanceObjectUpdate.as_view(), name='objects-detail'),
    path('objects/<int:pk>/delete', views.FinanceObjectDelete.as_view(), name='objects-delete'),
    path('objects/all', views.FinanceObjectList.as_view(), name='objects-all'),

    path('day_reports/new', views.DayReportCreate.as_view(), name='day_reports-create'),
    path('day_reports/<int:pk>', views.DayReportUpdate.as_view(), name='day_reports-detail'),
    path('day_reports/<int:pk>/delete', views.DayReportDelete.as_view(), name='day_reports-delete'),
    path('day_reports/all', views.DayReportList.as_view(), name='day_reports-all'),
]
