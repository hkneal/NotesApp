from django.shortcuts import render, redirect

#Required to handle Login/Registration authentication and forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from .models import Note, Label
from .forms import SignupForm, LoginForm, CreateNoteForm, CreateLabelForm

#Handle Email message for registration token and authentication
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token


FIRSTLIST = ['first_name', 'last_name', 'email']

#Simplification Methods
#has this user been authenticated
def checkAuth(req):
    if req.user.is_authenticated:
        return True
    else:
        return False

def generateContext():
    context = {
        'firstList' : FIRSTLIST,
        'signupForm' : SignupForm(),
        'loginForm' : LoginForm()
    }
    return context

def generateNotesList(req):
    user = req.user
    notes = user.note_set.all()
    return notes

def returnHome():
    context = {
        'error_message' : "You must be logged in to perform that function!",
        **generateContext()
    }
    return context

#Update and Delete View Classes
class NoteUpdate(UpdateView):
    model = Note
    fields = ['title', 'note']
    template_name_suffix = 'Update_Form'

class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('accounts')
    success_message = "Note was successfully deleted!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message)
        return super(NoteDelete, self).delete(request, *args, **kwargs)

#Begin view definitions
def index(req):
    #Return to home if user is logged in and authenticated
    if(checkAuth(req)):
        notes = generateNotesList(req)
        context = {
            'user' : req.user,
            'notes_List' : notes
            }
        return render(req, 'notes_app/notesPage.html', context)

    #Seperate the signup form into two smaller groups for stepper in index.html
    context={
        'gotodiv' : "step-2",
        **generateContext()
        }

    return render(req, 'notes_app/index.html', context)

#!!!!! Update this to be the logged in home page
def accounts(req):
    if (checkAuth(req)):
        notes = generateNotesList(req)
        context = {
            'notes_List': notes,
            'user' : req.user
            }
        return render(req, 'notes_app/notesPage.html', context)
    else:
        context = generateContext()
        return render(req, 'notes_app/index.html', context)


def signup(req):
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(req)
            mail_subject = 'Activate NotesApp Account.'
            message = render_to_string('notes_app/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),  #Django 1.1
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(), #Django 2.0
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            context= {
                'gotodiv' : 'step-3',
                'success_message' : 'Please confirm your email address to complete the registration',
                **generateContext()
            }

            # return to #step-4 on the index page
            return render(req, 'notes_app/index.html', context)
        else:
            #return HttpResponse('Activation link is invalid!')
            context = {
                'firstList' : FIRSTLIST,
                'signupForm' : form,
                'loginForm' : LoginForm(),
                'error_message' : 'Signup information is incorrect!'
            #Handle the retuned messages from the login form
            }
            return render(req, 'notes_app/index.html', context)
    else:
        if (checkAuth(req)):
            notes = generateNotesList(req)
            context = {
                'notes_List': notes,
                'user': req.user
                }
            return render(req, 'notes_app/notesPage.html', context)
        else:
            context = generateContext()
            return render(req, 'notes_app/index.html', context)

def Login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        form = LoginForm(data=req.POST)
        if user is not None:
            login(req, user)
        # if form.is_valid():
            notes = generateNotesList(req)
            context = {
            'user': user,
            'success_message' : 'You are Now Logged In!',
            'notes_List' : notes
            }
            return render(req, 'notes_app/notesPage.html', context)
        else:
            #return HttpResponse('Activation link is invalid!')
            context = {
            'firstList' : FIRSTLIST,
            'gotodiv' : 'step-3',
            'loginForm' : form,
            'signupForm' : SignupForm(),
            'error_message' : 'Login information is incorrect!'
            #Handle the retuned messages from the login form
            }
            return render(req, 'notes_app/index.html', context)
    else:
        context = generateContext()
    return render(req, 'notes_app/index.html', context)

def activate(req, uidb64, token):
    try:
        # uid = force_text(urlsafe_base64_decode(uidb64)) #Django 1.1
        uid = urlsafe_base64_decode(uidb64).decode()  #Django 2.0
        # print(uid)
        user = User.objects.get(pk=uid)
        # print(user)
    except TypeError:
        print("TypeError")
    except ValueError:
        print("ValueError")
    except OverflowError:
        print("OverflowError")
    except User.DoesNotExist:
        print("No user")
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(req, user)
        # return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        notes = generateNotesList(req)
        context = {
            'user' : user,
            'notes_List': notes,
            'success_message' : 'Thank you for your email confirmation. You are now Logged In!'
            }
        return render(req, 'notes_app/notesPage.html', context)
    else:
        #return HttpResponse('Activation link is invalid!')
        print(account_activation_token.check_token(user, token))
        print(user)
        context = {
            'error_message' : 'Activation link is invalid!',
            **generateContext()
            }
        return render(req, 'notes_app/index.html', context)

@login_required
def createNote(req):
    if (checkAuth(req)):
        user = req.user
        if req.method == 'POST':
            form = CreateNoteForm(req.POST)
            if form.is_valid():
                myNote = Note.objects.create(
                notes_list_id = user.id,
                title = form.cleaned_data['title'],
                note = form.cleaned_data['note']
                )

                #Collect all of the notes created by our Authenticated User
                notes = generateNotesList(req)

                context = {
                    'user': user,
                    'notes_List': notes,
                    'success_message' : 'You have created a new note!'
                }
                return render(req, 'notes_app/notesPage.html', context)
            else:
                context = {
                    'user': user,
                    'error_message' : "Form is Invalid!",
                    'createNoteForm' : form
                }
                return render(req, 'notes_app/notesPage.html', context)

        else:
            context = {
            'user' : user,
            'createNoteForm' : CreateNoteForm()
            }
            return render(req, 'notes_app/notesPage.html', context)
    else:
        context = returnHome()
        return render(req, 'notes_app/index.html', context)

@login_required
def createLabel(req, pk):
    print("In createLabel")
    if (checkAuth(req)):
        user = req.user
        if req.method == 'POST':
            form = CreateLabelForm(req.POST)
            if form.is_valid():
                Label.objects.create(
                labels_list_id = pk,
                label = form.cleaned_data['label']
                )
                notes = generateNotesList(req)
                context = {
                    'user': user,
                    'notes_List': notes,
                    'success_message' : 'Note Label Created!'
                }
                return render(req, 'notes_app/notesPage.html', context)
            else:
                context = {
                    'user': user,
                    'error_message' : "Form is Invalid!",
                    'createLabelForm' : form
                }
                return render(req, 'notes_app/notesPage.html', context)
        else:
            noteTitle = Note.objects.get(id=pk).title
            context = {
                'user': user,
                'note_id' : pk,
                'noteTitle' : noteTitle,
                'createLabelForm' : CreateLabelForm()
            }
            return render(req, 'notes_app/notesPage.html', context)
    else:
        context = returnHome()
        return render(req, 'notes_app/index.html', context)

@login_required
def searchLabel(req, id):
    pass
    #add a view for current labels in modal
    #Used to collect the ForeignKey path back up to User, reduces DB hits
    # notes = user.note_set.all()
    # myLabel = Label.objects.select_related('notes__users').get(notes_id=id)
    #
    # myNote = myLabel.notes
    # myUser = myNote.users
    # print(myNote.title)
    # print(myUser.first_name)

def Logout(req):
    if (checkAuth(req)):
        logout(req)
        logged_in = False
        context = {
            'success_message' : ' You Have Logged Out',
            **generateContext()
        }
        return render(req, 'notes_app/index.html', context)
    else:
        context = generateContext()
        return render(req, 'notes_app/index.html', context)
