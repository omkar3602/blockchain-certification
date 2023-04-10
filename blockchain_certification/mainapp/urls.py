from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('issue_certificate/', views.issue_certificate, name='issue_certificate'),
    path('view_all/', views.view_all, name='view_all'),

    path('view/', views.view, name='view'),
    path('certificate/<str:id>', views.certificate, name='certificate'),
    path('issued_certificates/', views.issued_certificates, name='issued_certificates'),
]