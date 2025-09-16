# backend/project_tracker/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg

from .models import MiniProject
from .serializers import MiniProjectSerializer
from .permissions import IsTrainerOrAssignedTrainee


class MiniProjectViewSet(viewsets.ModelViewSet):
    queryset = MiniProject.objects.select_related("assigned_to", "created_by").all()
    serializer_class = MiniProjectSerializer
    permission_classes = [IsAuthenticated, IsTrainerOrAssignedTrainee]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["status", "priority", "assigned_to__id", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        # If trainee, only show their own assigned projects
        if not self.request.user.is_staff:
            qs = qs.filter(assigned_to=self.request.user)
        return qs


# ---------------- Extra endpoints ---------------- #

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_trainer": bool(user.is_staff),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reports(request):
    # trainer-only
    if not request.user.is_staff:
        return Response({"detail": "Forbidden"}, status=403)

    total = MiniProject.objects.count()
    by_status = list(MiniProject.objects.values("status").annotate(count=Count("id")))
    avg_progress = MiniProject.objects.aggregate(avg_progress=Avg("progress"))["avg_progress"] or 0
    completed = MiniProject.objects.filter(status="completed").count()

    return Response({
        "total": total,
        "by_status": by_status,
        "avg_progress": avg_progress,
        "completed": completed,
    })
