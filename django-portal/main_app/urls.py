from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('locations/', views.LocationList.as_view(), name="location-list"),
    path('locations/new/', views.LocationCreate.as_view(), name="location_create"),
    path('locations/<int:pk>/', views.LocationDetail.as_view(), name="location_detail"),
    path('locations/<int:pk>/update', views.LocationUpdate.as_view(), name="location_update"),
    path('locations/<int:pk>delete', views.LocationDelete.as_view(), name="location_delete"),
    path('user/<username>/', views.profile, name='profile'),
    path('reports/', views.reports_index, name='reports_index'),
    path('reports/<int:report_id>', views.reports_show, name='reports_show'),
    path('reports/create/', views.ReportCreate.as_view(), name='reports_create'),
    path('reports/<int:pk>/update/', views.ReportUpdate.as_view(), name='reports_update'),
    path('reports/<int:pk>/delete/', views.ReportDelete.as_view(), name='reports_delete'),  
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]