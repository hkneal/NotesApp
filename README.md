# NotesApp
Repository for the NotesApp API and Web Application

# Website URL
<https://InputMyNote.com>

# API Endpoints

/api/note/  (GET / POST)

    Returns a list of your notes or allows a POST of a single note
    
/api/label/ (GET / POST) 

    Returns a list of labels associated with your notes or allows a POST of a single label
    
/api/note/<int:pk>/ (GET) 

    Returns a specific note (by id num) 
   
/api/label/<int:pk>/ (GET)

    Returns a specific label
    
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

/rest-auth/password/change/ (POST)

    new_password1
    new_password2
    old_password
    
/rest-auth/user/ (GET, PUT, PATCH)

    username
    first_name
    last_name
    Returns pk, username, email, first_name, last_name
    


#API Registration

/rest-auth/registration/ (POST)

    username
    password1
    password2
    email
    
/rest-auth/registration/verify-email/ (POST)

    key
    
# Installation

    Pull repository and from a terminal window navigate into the NotesApp folder.
    $cd NotesApp

Install & start virtualenv, these commands are issued from a terminal command within the 
    
    $ pip install virtualenv
    $ virtualenv <virtualenv name>
    $ source <virtualenv name>/bin/activate
    
Install system requirements

    $ brew install Python3
        for instructions on how to install Homebrew (brew) => https://www.howtogeek.com/211541/homebrew-for-os-x-easily-installs-desktop-apps-and-terminal-utilities/
        
    $ pip install 3.6-dev
    
    - Navigate into the "notes" folder where you will find "requirements.txt" file
    $ cd notes
    $ pip install -r requirements.txt
    $ export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
    
    - Navigate into the app folder
    $ cd notes  //again you sould now be at NotesApp/notes/notes
    
    - create settings.ini & notesCNF.cnf files:
    
        settings.ini:
        
        [settings]
        SECRET_KEY = 8qlg)=96i@@&y5u!&6qc(w_b4nay3+wvpx&!uibp9utjuknj!d
        EMAIL_USE_TLS = True
        EMAIL_HOST = <your email host>
        EMAIL_HOST_USER = <emai username>
        EMAIL_HOST_PASSWORD = <email password>
        EMAIL_PORT = 587
        DEFAULT_FROM_EMAIL = Adminstrator <admin@inputmynote.awsapps.com>
        AWS_ACCESS_KEY_ID = <your AWS access ID>
        AWS_SECRET_ACCESS_KEY = <your AWS access key>
        
        notes.CNF.cnf:
        
        [client]
        name = notesApp
        host = localhost
        user = root
        password = <your MySQL password>
        default-character-set = utf8MB4
    
    Connect to your MySQL Database
    $ mysql -u root -p (then enter password at prompt)
    > CREATE DATABASE notesAPP
    > exit
    
    Setup and start Django 
    $ cd .. (should now be in NotesApp/notes)
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver
    

