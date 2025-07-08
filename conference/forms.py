from django import forms
from .models import AbstractSubmission, CoAuthor

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
            'abstract_file'
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

class FullPaperUploadForm(forms.ModelForm):
    class Meta:
        model = AbstractSubmission
        fields = ['full_paper']
        widgets = {
            'full_paper': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }

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
