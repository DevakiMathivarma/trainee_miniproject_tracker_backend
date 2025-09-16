# backend/project_tracker/serializers.py
from rest_framework import serializers
from .models import MiniProject
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")

class MiniProjectSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="assigned_to", required=False, allow_null=True
    )
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = MiniProject
        fields = ("id","title","description","assigned_to","assigned_to_id","created_by","priority","status","due_date","progress","created_at","updated_at")
        read_only_fields = ("id","created_by","created_at","updated_at")
