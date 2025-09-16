# project_tracker/permissions.py
from rest_framework import permissions

class IsTrainerOrAssignedTrainee(permissions.BasePermission):
    """
    Trainers (is_staff=True) have full access.
    Authenticated trainees can list/retrieve, but object-level checks enforce
    that they can only retrieve/update their own assigned projects.
    Only trainers can create or delete.
    """

    def has_permission(self, request, view):
        action = getattr(view, "action", None)

        # Allow unauthenticated safe methods? we require authentication
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        # Create and delete restricted to trainers
        if action in ("create", "destroy"):
            return bool(request.user and request.user.is_staff)

        # For other methods (update/partial_update) allow authenticated; object-level will refine
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Trainers can do anything
        if request.user and request.user.is_staff:
            return True

        action = getattr(view, "action", None)
        # Allow trainees to view only if assigned
        if request.method in permissions.SAFE_METHODS or action == "retrieve":
            return obj.assigned_to == request.user

        # Allow trainees to update/partial_update only on their assigned objects
        if action in ("update", "partial_update") or request.method in ("PUT", "PATCH"):
            return obj.assigned_to == request.user

        # Default deny (including delete)
        return False
