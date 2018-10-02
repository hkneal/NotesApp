#from django.conf.urls import url   > This was used with Django 1.11
#from django.urls.re_path			> The Old function is still available with this class
from django.conf.urls import url
from django.urls import path, include

from django.contrib.auth import views as auth_views
from . import views

from .forms import LoginForm

urlpatterns = [
  path('', views.index, name='index'),
  path('index/', views.index, name='index'),  	#With Django 2.0
  path('signup/', views.signup, name='signup'),
  path('accounts/', views.accounts, name='accounts'),
  path('accounts/search/', views.search, name='search'),
  path('accounts/login/', auth_views.LoginView.as_view(template_name='notes_app/registration/login.html', authentication_form=LoginForm), name='login'),
  path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='notes_app/registration/password_reset_form.html'), name='reset'),
  path('accounts/password_reset/done/', auth_views.PasswordResetView.as_view(template_name='notes_app/registration/password_reset_done.html')),
  path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='notes_app/registration/password_reset_confirm.html')),
  path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='notes_app/registration/password_reset_complete.html')),
  path('accounts/', include('django.contrib.auth.urls')),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('accounts/createNote', views.NoteCreate.as_view(), name='createNote'),
  path('accounts/createLabel/<int:pk>/', views.LabelCreate.as_view(), name='createLabel'),
  path('accounts/update/<int:pk>/', views.NoteUpdate.as_view(), name='updateNote'),
  path('accounts/<int:pk>/delete', views.NoteDelete.as_view(), name='delete_note'),


]
