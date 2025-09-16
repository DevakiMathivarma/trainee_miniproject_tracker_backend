# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# import the functions you added
from project_tracker.views import me, reports

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user info endpoint
    path('api/auth/me/', me),

    # trainer-only reports endpoint
    path('api/reports/', reports),

    # app router (mini-projects)
    path('api/', include('project_tracker.urls')),
]
