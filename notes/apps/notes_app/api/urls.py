from django.urls import path   			#Used with Django 2.0
from .views import NotesApiRUDView, LabelApiRUDView, NotesApiView, LabelApiView

#Enable Token via POST with username and password
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
  # url(r'^$', views.index),   This is used in Django 1.11

  path('', NotesApiView.as_view(), name='notes'),
  path('labels/', LabelApiView.as_view(), name='labels'),  	#With Django 2.0
  path('<int:pk>/', NotesApiRUDView.as_view(), name='note_api_RUD'),
  path('label/<int:pk>/', LabelApiRUDView.as_view(), name='label_api_RUD'),
  path('api-token-auth/', obtain_jwt_token),
  path('api-token-refresh/', refresh_jwt_token),
  path('api-token-verify', verify_jwt_token)

]
