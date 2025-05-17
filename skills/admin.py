from django.contrib import admin
from .models import Skill, SkillCategory

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'proficiency', 'created_at')
    list_filter = ('category', 'user')
    search_fields = ('name', 'user__username')

admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillCategory)