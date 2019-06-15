from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/', views.employee_view, name='employee'),
    path('employee', views.employee_view, name='employee'),
    path('department/', views.department_view, name='department'),
]