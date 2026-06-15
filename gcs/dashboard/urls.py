from django.urls import path
from .views import dashboard_content, dashboard_change, check

urlpatterns = [
    path('content/', dashboard_content, name='dashboard-content'),
    path('change-dashboard/', dashboard_change, name='dashboard-change'),
    path('/check/', check, name='check')
]
