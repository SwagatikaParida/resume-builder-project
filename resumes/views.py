from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
from .models import Resume, UserProfile
from .forms import ResumeForm, UserProfileForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm

def home(request):
    if request.user.is_authenticated:
        return redirect('resume_list')
    return render(request, 'resumes/home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'resumes/signup.html', {'form': form})

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(owner=request.user)
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.owner = request.user
            resume.save()
            messages.success(request, 'Resume created successfully!')
            return redirect('resume_list')
    else:
        form = ResumeForm()
    return render(request, 'resumes/resume_form.html', {'form': form, 'title': 'Create Resume'})

@login_required
def resume_update(request, pk):
    resume = get_object_or_404(Resume, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume updated successfully!')
            return redirect('resume_list')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resumes/resume_form.html', {'form': form, 'title': 'Update Resume'})

@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, owner=request.user)
    return render(request, 'resumes/resume_detail.html', {'resume': resume})

@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, owner=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
        return redirect('resume_list')
    return render(request, 'resumes/resume_confirm_delete.html', {'resume': resume})

@login_required
def generate_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, owner=request.user)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leading=14
    )
    
    story = []

    # Header with name
    story.append(Paragraph(resume.full_name, title_style))
    story.append(Spacer(1, 20))

    # Contact Information Section
    contact_info = []
    contact_info.append(f"Email: {resume.email}")
    if resume.phone:
        contact_info.append(f"Phone: {resume.phone}")
    if resume.address:
        contact_info.append(f"Address: {resume.address}")
    
    if contact_info:
        story.append(Paragraph("Contact Information", heading_style))
        for info in contact_info:
            story.append(Paragraph(info, normal_style))
        story.append(Spacer(1, 15))

    # Online Presence
    online_info = []
    if resume.linkedin:
        online_info.append(f"LinkedIn: {resume.linkedin}")
    if resume.github:
        online_info.append(f"GitHub: {resume.github}")
    if resume.portfolio:
        online_info.append(f"Portfolio: {resume.portfolio}")
    
    if online_info:
        story.append(Paragraph("Online Presence", heading_style))
        for info in online_info:
            story.append(Paragraph(info, normal_style))
        story.append(Spacer(1, 15))

    # Professional Summary
    if resume.summary:
        story.append(Paragraph("Professional Summary", heading_style))
        story.append(Paragraph(resume.summary, normal_style))
        story.append(Spacer(1, 15))

    # Skills Section
    if resume.skills:
        story.append(Paragraph("Skills", heading_style))
        # Split skills by comma or newline and format nicely
        skills_list = [skill.strip() for skill in resume.skills.replace('\n', ',').split(',') if skill.strip()]
        skills_text = " • " + "\n • ".join(skills_list)
        story.append(Paragraph(skills_text, normal_style))
        story.append(Spacer(1, 15))

    # Languages Section
    if resume.languages:
        story.append(Paragraph("Languages", heading_style))
        # Handle multi-line language entries
        language_lines = resume.languages.split('\n')
        for line in language_lines:
            if line.strip():
                story.append(Paragraph(" • " + line.strip(), normal_style))
        story.append(Spacer(1, 15))

    # Work Experience
    if resume.experience:
        story.append(Paragraph("Work Experience", heading_style))
        # Handle multi-line experience entries
        experience_lines = resume.experience.split('\n')
        for line in experience_lines:
            if line.strip():
                story.append(Paragraph(line.strip(), normal_style))
        story.append(Spacer(1, 15))

    # Education
    if resume.education:
        story.append(Paragraph("Education", heading_style))
        # Handle multi-line education entries
        education_lines = resume.education.split('\n')
        for line in education_lines:
            if line.strip():
                story.append(Paragraph(line.strip(), normal_style))
        story.append(Spacer(1, 15))

    # Certifications
    if resume.certifications:
        story.append(Paragraph("Certifications", heading_style))
        # Handle multi-line certification entries
        cert_lines = resume.certifications.split('\n')
        for line in cert_lines:
            if line.strip():
                story.append(Paragraph(" • " + line.strip(), normal_style))
        story.append(Spacer(1, 15))

    # Projects & Achievements
    if resume.projects:
        story.append(Paragraph("Projects & Achievements", heading_style))
        # Handle multi-line project entries
        project_lines = resume.projects.split('\n')
        for line in project_lines:
            if line.strip():
                story.append(Paragraph(line.strip(), normal_style))
        story.append(Spacer(1, 15))

    # Interests & Hobbies
    if resume.interests:
        story.append(Paragraph("Interests & Hobbies", heading_style))
        story.append(Paragraph(resume.interests, normal_style))
        story.append(Spacer(1, 15))

    # Professional References
    if resume.references:
        story.append(Paragraph("Professional References", heading_style))
        # Handle multi-line reference entries
        ref_lines = resume.references.split('\n')
        for line in ref_lines:
            if line.strip():
                story.append(Paragraph(line.strip(), normal_style))

    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name.replace(" ", "_")}_resume.pdf"'
    return response

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'resumes/profile.html', {'user_profile': user_profile})

@login_required
def profile_edit(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'resumes/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'resumes/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', '')
        if confirmation == 'DELETE':
            # Delete the user account
            user = request.user
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please type "DELETE" to confirm account deletion.')

    return render(request, 'resumes/delete_account.html')
