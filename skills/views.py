from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Skill
from .forms import SkillForm
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import pandas as pd

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    skills = Skill.objects.filter(user=request.user)
    total_skills = skills.count()
    
    if total_skills > 0:
        avg_proficiency = sum(skill.proficiency for skill in skills) / total_skills
    else:
        avg_proficiency = 0
    
    # Prepare data for charts
    categories = {}
    proficiency_levels = {i: 0 for i in range(1, 11)}
    
    for skill in skills:
        categories[skill.category] = categories.get(skill.category, 0) + 1
        proficiency_levels[skill.proficiency] += 1
    
    context = {
        'skills': skills,
        'total_skills': total_skills,
        'avg_proficiency': round(avg_proficiency, 1),
        'categories': json.dumps(categories),
        'proficiency_levels': json.dumps(proficiency_levels),
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    skills = Skill.objects.filter(user=request.user)
    total_skills = skills.count()
    
    if total_skills > 0:
        avg_proficiency = sum(skill.proficiency for skill in skills) / total_skills
    else:
        avg_proficiency = 0
    
    context = {
        'user': request.user,
        'skills': skills,
        'total_skills': total_skills,
        'avg_proficiency': round(avg_proficiency, 1),
    }
    
    return render(request, 'profile.html', context)

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('dashboard')
    else:
        form = SkillForm()
    
    return render(request, 'add_skill.html', {'form': form})

@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)
    
    return render(request, 'edit_skill.html', {'form': form, 'skill': skill})

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'delete_skill.html', {'skill': skill})

@login_required
def export_profile(request, format):
    skills = Skill.objects.filter(user=request.user)
    data = {
        'username': request.user.username,
        'email': request.user.email,
        'skills': [
            {
                'name': skill.name,
                'category': skill.category,
                'proficiency': skill.proficiency,
                'created_at': skill.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': skill.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for skill in skills
        ]
    }
    
    if format == 'json':
        response = JsonResponse(data, json_dumps_params={'indent': 4})
        response['Content-Disposition'] = f'attachment; filename={request.user.username}_skills.json'
        return response
    
    elif format == 'csv':
        df = pd.DataFrame(data['skills'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={request.user.username}_skills.csv'
        df.to_csv(response, index=False)
        return response
    
    elif format == 'pdf':
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # PDF content
        p.drawString(100, 750, f"Skill Profile: {request.user.username}")
        p.drawString(100, 730, f"Email: {request.user.email}")
        p.drawString(100, 710, f"Total Skills: {len(data['skills'])}")
        
        y = 680
        p.drawString(100, y, "Skills:")
        y -= 20
        
        for skill in data['skills']:
            p.drawString(120, y, f"- {skill['name']} ({skill['category']}): {skill['proficiency']}/10")
            y -= 15
            if y < 50:  # New page if we're at the bottom
                p.showPage()
                y = 750
        
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={request.user.username}_skills.pdf'
        return response
    
    return redirect('profile')