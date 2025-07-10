from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AbstractSubmission, CoAuthor, UserProfile

from django.core.exceptions import ValidationError


# ----------- Signup Form (NEW) -----------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    institute = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'institute', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Save profile info
            profile = user.userprofile
            profile.phone_number = self.cleaned_data['phone_number']
            profile.institute = self.cleaned_data['institute']
            profile.save()
        return user


# ----------- Abstract Submission Form -----------
DESIGNATION_CHOICES = [
    ('Student', 'Student'),
    ('Research Scholar', 'Research Scholar'),
    ('Professor', 'Professor'),
    ('Associate Professor', 'Associate Professor'),
    ('Assistant Professor', 'Assistant Professor'),
    ('Corporate', 'Corporate'),
]

class AbstractSubmissionForm(forms.ModelForm):
    designation = forms.ChoiceField(
        choices=[('', '---------')] + DESIGNATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = AbstractSubmission
        fields = [
            'title',
            'name',
            'institute',
            'custom_institute',
            'designation',
            'keywords',
            'abstract_file',
            'mode_of_participation',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'custom_institute': forms.TextInput(attrs={'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'abstract_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
            'institute': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        institute = cleaned_data.get('institute')
        custom_institute = cleaned_data.get('custom_institute')

        if institute == 'Others' and not custom_institute:
            self.add_error('custom_institute', "Please enter your institute name.")

    def clean_abstract_file(self):
        file = self.cleaned_data.get('abstract_file')
        if file:
            allowed_types = [
                'application/pdf',
                'application/msword',  # .doc
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # .docx
            ]
            if file.content_type not in allowed_types:
                raise ValidationError("Unsupported file type. Upload PDF or Word document (.pdf, .doc, .docx).")
        return file

class FullPaperUploadForm(forms.ModelForm):
    class Meta:
        model = AbstractSubmission
        fields = ['full_paper']
        widgets = {
            'full_paper': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }

    def clean_full_paper(self):
        file = self.cleaned_data.get('full_paper')
        if file and file.content_type != 'application/pdf':
            raise ValidationError("Only PDF files are allowed for full paper upload.")
        return file


# ----------- Co-Author Form -----------
class CoAuthorForm(forms.ModelForm):
    designation = forms.ChoiceField(
        choices=[('', '---------')] + DESIGNATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = CoAuthor
        fields = ['first_name', 'last_name', 'email', 'designation']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
