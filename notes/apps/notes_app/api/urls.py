from django.urls import path, include   			#Used with Django 2.0
from . import views

urlpatterns = [
  # url(r'^$', views.index),   This is used in Django 1.11

  path('notes/', views.NotesApiView.as_view(), name='notes'),
  path('labels/', views.LabelApiView.as_view(), name='labels'),  	#With Django 2.0
  path('note/<int:pk>/', views.NotesApiRUDView.as_view(), name='note_api_RUD'),
  path('label/<int:pk>/', views.LabelApiRUDView.as_view(), name='label_api_RUD'),
  path('rest_auth/', include('rest_auth.urls')),
]
