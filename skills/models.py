from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class SkillCategory(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Programming', 'Programming'),
        ('Frameworks', 'Frameworks'),
        ('Databases', 'Databases'),
        ('DevOps', 'DevOps'),
        ('Design', 'Design'),
        ('Others', 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) - {self.proficiency}/10"
    
    class Meta:
        ordering = ['-proficiency', 'name']