from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Resume(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    # New creative fields
    address = models.CharField(max_length=200, blank=True, help_text="Your current address")
    linkedin = models.URLField(blank=True, help_text="LinkedIn profile URL")
    github = models.URLField(blank=True, help_text="GitHub profile URL")
    portfolio = models.URLField(blank=True, help_text="Portfolio website URL")
    languages = models.TextField(blank=True, help_text="Languages you speak (e.g., English: Native, Spanish: Intermediate)")
    certifications = models.TextField(blank=True, help_text="Professional certifications")
    projects = models.TextField(blank=True, help_text="Notable projects or achievements")
    interests = models.TextField(blank=True, help_text="Personal interests and hobbies")
    references = models.TextField(blank=True, help_text="Professional references")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.owner.username})"
