import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accountapp import views as accountapp_views

router = DefaultRouter()
router.register("accounts", accountapp_views.UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path("__debug__/", include(debug_toolbar.urls)),
    ]