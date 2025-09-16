# backend/project_tracker/models.py
from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = (
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
)

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("inprogress", "In Progress"),
    ("completed", "Completed"),
)

class MiniProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, related_name="mini_projects", on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="created_mini_projects", on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    due_date = models.DateField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"
