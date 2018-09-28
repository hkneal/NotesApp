from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Note, Label

def validateName(strInput):
    if not strInput.replace(' ','').isalpha():
        return False
    if len(strInput) < 3 or len(strInput > 35):
        return False
    return True

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control validate'}), required=True, min_length=8, max_length=150, help_text='A Unique Username is Required, Username Must be at least 8 characters')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control validate'}), max_length=254,required=True, help_text='A Unique Email Address is Required (myName@Example.com).')
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control validate'}), min_length=2, max_length=35, required=True, help_text='Must be at least 2 characters and less than 45 characters (no numbers or symbols)')
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control validate'}), min_length=2, max_length=35, required=True, help_text='Must be at least 2 characters and less than 45 characters (no numbers or symbols)')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class': 'form-control validate'}), required=True, min_length=8, max_length=45, help_text='Password Must be at least 8 characters')
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control validate'}), required=True, min_length=8, max_length=150, help_text='Confirm Password Must Match Password')

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control validate'}), required=True, min_length=8, max_length=150, help_text='Please enter in your Username')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class': 'form-control validate'}), required=True, min_length=8, max_length=45, help_text='Password Must be at least 8 characters')
    class Meta:
        model = User
        fields = ('username', 'password')

class CreateNoteForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control validate', 'placeholder' : 'Add Title (required)' }),required=True, max_length=45, help_text='Title must be less than 45 characters')
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control validate', 'placeholder' : 'Note (required)'}), required=True, max_length=500, help_text='You can\'t create a note without typing in the note :)')

    class Meta:
        model = Note
        fields = ('title', 'note')

    def clean_note(self):
        thisNote = self.cleaned_data['note']
        if not thisNote:
            raise ValidationError('You can\'t create a note without typing in the note :)')
        if len(thisNote) > 500:
            raise ValidationError('Note Should Be Less Than 500 Characters')
        return thisNote

class CreateLabelForm(forms.Form):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control validate'}),required=True, max_length=45, help_text='Label must be less than 45 characters')

    class Meta:
        model = Note
        fields = ('label')
