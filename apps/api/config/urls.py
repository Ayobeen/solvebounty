from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def health_check(request):
    db_status = "ok"
    try:
        connection.ensure_connection()
    except Exception as e:
        db_status = f"error: {str(e)}"
    return JsonResponse({
        "status": "ok",
        "database": db_status,
        "version": "1.0.0",
        "market": "Nigeria"
    })

api_v1_patterns = [
    path('health/', health_check, name='health-check'),
    path('auth/', include('apps.accounts.urls')),
    path('', include('apps.profiles.urls')),
    path('skills/', include('apps.skills.urls')),
    path('challenges/', include('apps.challenges.urls')),
    path('', include('apps.submissions.urls')),
    path('payments/', include('apps.payments.urls')),
    path('payouts/', include('apps.payouts.urls')),
    path('ledger/', include('apps.ledger.urls')),
    path('disputes/', include('apps.disputes.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('audit/', include('apps.audit.urls')),
    path('ai/', include('apps.ai_client.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_patterns)),
    
    # OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
