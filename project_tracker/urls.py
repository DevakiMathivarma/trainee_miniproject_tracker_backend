# backend/project_tracker/urls.py
from rest_framework.routers import DefaultRouter
from .views import MiniProjectViewSet

router = DefaultRouter()
router.register(r'mini-projects', MiniProjectViewSet, basename='mini-project')

urlpatterns = router.urls
