# backend/project_tracker/admin.py
from django.contrib import admin
from .models import MiniProject

@admin.register(MiniProject)
class MiniProjectAdmin(admin.ModelAdmin):
    list_display = ('title','status','priority','assigned_to','created_by','due_date')
