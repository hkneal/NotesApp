# NotesApp
Repository for the NotesApp API and Web Application

# Website URL
http://InputMyNote.com

# API Endpoints
/rest-auth/login/ (POST) 

    username
    email
    password
    Returns Token key
    
/rest-auth/logout/ (POST)

/rest-auth/password/reset/ (POST)
    email
    
/rest-auth/password/reset/confirm/ (POST)

    uid
    token
    new_password1
    new_password2

http://inputmynote/api/note/  GET a list of your notes or POST a single note
http://inputmynote/api/label/ GET a list of labels associated with your notes or POST a label
http://inputmynote/api/note/<int:pk>/ GET a specific note (by id num) 
http://inputmynote/api/label/<int:pk>/ GET a specific label
http://inputmynote/api/rest_auth/password/reset/ Reset the 
http://inputmynote/api/rest_auth/password/reset/confirm/$ [name='rest_password_reset_confirm']
http://inputmynote/api/rest_auth/login/$ [name='rest_login']
http://inputmynote/api/rest_auth/logout/$ [name='rest_logout']
http://inputmynote/api/rest_auth/user/$ [name='rest_user_details']
http://inputmynote/api/rest_auth/password/change/$ [name='rest_password_change']
