#from django.conf.urls import url   > This was used with Django 1.11
#from django.urls.re_path			> The Old function is still available with this class
from django.conf.urls import url
from django.urls import path   			#Used with Django 2.0
from . import views

#Django 2.0 needed for namespace in main.urls

urlpatterns = [
  # url(r'^$', views.index),   This is used in Django 1.11
  # url(r'^api/post$', CreateView.as_view(), name="create")
  # path('home/pictures/<int:picNum')		#now recognized as int
  path('', views.index, name='index'),
  path('index', views.index, name='index'),  	#With Django 2.0
  path('signup', views.signup, name='signup'),
  path('accounts', views.accounts, name='accounts'),
  path('accounts/Login', views.Login, name='Login'),
  path('accounts/Logout', views.Logout, name='Logout'),
  # path('activate/<str:uid>/<str:token>', views.activate, name='activate'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('accounts/createNote', views.createNote, name='createNote'),
  path('accounts/createLabel/<int:pk>/', views.createLabel, name='createLabel'),
  path('accounts/update/<int:pk>/', views.NoteUpdate.as_view(), name='update_note'),
  path('accounts/<int:pk>/delete', views.NoteDelete.as_view(), name='delete_note'),
  # path('accounts/<int:pk>/delete', views.delete_note, name='delete_note'),
  # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
