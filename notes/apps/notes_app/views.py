from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Note, Label
from django.db.models import Q

from .forms import SignupForm, LoginForm, CreateNoteForm, CreateLabelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#Handle Email message for registration token and authentication
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.http import HttpResponse, Http404




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

#Update and Delete View Classes
#Create note, Create Label, and Update note use the same template, a check for object allows catering the template accordingly.
class NoteCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Note
    template_name_suffix = 'CreateUpdate_Form'
    form_class = CreateNoteForm
    success_url = reverse_lazy('accounts')
    success_message = "You created a new note!"

    #get the user.id for ForeignKey
    def form_valid(self, form):
        form.instance.notes = self.request.user
        return super(NoteCreate, self).form_valid(form)

class LabelCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Label
    template_name_suffix = 'CreateLabel_form'
    form_class = CreateLabelForm
    success_url = reverse_lazy('accounts')
    success_message = "You created a new label for your note!"

    #get the note.id for ForeignKey, passed from urls
    def form_valid(self, form):
        noteObj = Note.objects.get(pk=self.kwargs['pk'])
        form.instance.labels = noteObj
        if self.request.user != noteObj.notes:
            return Http404("You are not allowed to create a label on this note!")
        return super(LabelCreate, self).form_valid(form)

class NoteUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Note
    template_name_suffix = 'CreateUpdate_Form'
    form_class = CreateNoteForm
    success_url = reverse_lazy('accounts')
    success_message = "Your note was successfully updated!"

class NoteDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Note
    success_url = reverse_lazy('accounts')
    success_message = "Note was successfully deleted!"

    #overriding to generate succcess message, mixin isn't yet enabled for delete
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message)
        return super(NoteDelete, self).delete(request, *args, **kwargs)

#Begin view definitions
#Landing Page
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

#Main page for all Notes if user is authenticated
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
            #send_mail(mail_subject, message, 'admin@inputmynote.awsapps.com', [to_email], fail_silently=False,)

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

# @login_required
def search(req):
    print("in search")
    if(checkAuth(req)):
        if req.method=='POST':
            postData = req.POST['search_input']
            print(postData)
            
            #get all of the label objects containing our search string
            labelList = Label.objects.filter(Q(label__iexact=postData) |
                    Q(label__icontains=postData) |
                    Q(label__istartswith=postData) |
                    Q(label__iendswith=postData))
            #get the note object from the labels list & filter only user created
            user = req.user
            notes_from_lables = Note.objects.filter(Q(id__in=labelList.values('labels_id'))).filter(notes_id=user.pk)

            #get all note objects matching the search input & filter only user created
            noteslist = Note.objects.filter(Q(title__iexact=postData) |
                    Q(title__icontains=postData) |
                    Q(title__istartswith=postData) |
                    Q(title__iendswith=postData)).filter(notes_id=user.pk)

            if(noteslist.count()>0):
                print(noteslist.query)
            #merge the two querysets
            notes_search_List = noteslist.union(notes_from_lables)
        
            if(notes_search_List.count()>0):
                success_message = "These are your search results"
                context = {
                    'success_message' : success_message,
                    'notes_search_List' : notes_search_List
                    }
            else:
                error_message = "There were no notes containing that search input."
                context = {
                    'error_message' : error_message,
                    }
            return render(req, 'notes_app/notesPage.html', context)
        else:
            context = {
            'error_message' : 'Inactive method',
            **generateContext()
            }
            return render(req, 'notes_app/index.html', context)
    else:
        success_message = "Please log in to search through your personal notes."
        context = {
            'success_message' : success_message,
            **generateContext()
            }
        return render(req, 'notes_app/index.html', context)
