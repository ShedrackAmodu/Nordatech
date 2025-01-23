from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.login_with_token, name='login'),
    path('list/', views.document_list, name='list'),
    path('upload/', views.upload_document, name='upload'),
    path('logout/', views.logout_view, name='logout'),
    path('serve-pdf/<int:document_id>/', views.serve_pdf, name='serve_pdf'),  # New route
]
