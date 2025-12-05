from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
import re
from .models import Resume, UserProfile

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'email', 'phone', 'address', 'linkedin', 'github', 'portfolio', 'summary', 'skills', 'languages', 'experience', 'education', 'certifications', 'projects', 'interests', 'references']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, State, ZIP Code'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
            'portfolio': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a brief professional summary about yourself...'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List your key skills (e.g., Python, JavaScript, Project Management)'
            }),
            'languages': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Languages you speak:\nEnglish: Native\nSpanish: Intermediate\nFrench: Basic'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe your work experience:\n\nCompany Name | Position | Dates\n- Responsibility 1\n- Responsibility 2\n\nCompany Name | Position | Dates\n- Responsibility 1\n- Responsibility 2'
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'List your educational background:\n\nDegree | Institution | Year\n- Relevant coursework or achievements\n\nDegree | Institution | Year\n- Relevant coursework or achievements'
            }),
            'certifications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Professional certifications:\nAWS Certified Solutions Architect\nGoogle Cloud Professional Developer\nCertified Scrum Master'
            }),
            'projects': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Notable projects:\n\nProject Name | Technologies Used\n- Description of your role and achievements\n\nProject Name | Technologies Used\n- Description of your role and achievements'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Personal interests and hobbies:\nPhotography, Traveling, Open Source Contributions'
            }),
            'references': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Professional references:\n\nJohn Doe | Senior Manager | Company Inc.\nEmail: john.doe@company.com | Phone: (555) 123-4567\n\nJane Smith | Team Lead | Tech Corp\nEmail: jane.smith@techcorp.com | Phone: (555) 987-6543'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Address',
            'linkedin': 'LinkedIn Profile',
            'github': 'GitHub Profile',
            'portfolio': 'Portfolio Website',
            'summary': 'Professional Summary',
            'skills': 'Skills & Technologies',
            'languages': 'Languages',
            'experience': 'Work Experience',
            'education': 'Education',
            'certifications': 'Certifications',
            'projects': 'Projects & Achievements',
            'interests': 'Interests & Hobbies',
            'references': 'Professional References',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'phone', 'location', 'website', 'linkedin', 'github']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
        }
        labels = {
            'profile_picture': 'Profile Picture',
            'bio': 'Bio',
            'phone': 'Phone',
            'location': 'Location',
            'website': 'Website',
            'linkedin': 'LinkedIn',
            'github': 'GitHub',
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = ['gmail.com', 'google.com', 'googlemail.com']
        if email:
            domain = email.split('@')[-1]
            if domain not in allowed_domains:
                raise ValidationError(f"Email domain must be one of: {', '.join(allowed_domains)}.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.match(r'^[a-zA-Z0-9_.]+$', username):
            raise ValidationError("Username must contain only letters, numbers, underscores, and periods.")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password and not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not first_name.isalpha():
            raise ValidationError("First name must contain only alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not all(c.isalpha() or c.isspace() for c in last_name):
            raise ValidationError("Last name must contain only alphabetic characters and spaces.")
        return last_name

class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
