import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from accountapp import views as accountapp_views
from worldcupapp import views as worldcupapp_views

router = DefaultRouter()
router.register("accounts", accountapp_views.UserViewSet)
router.register("worldcups", worldcupapp_views.WorldcupViewSet)
router.register("albums", worldcupapp_views.AlbumViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", obtain_jwt_token),
    path("api/token/refresh/", refresh_jwt_token),
    path("api/token/verify/", verify_jwt_token),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path("__debug__/", include(debug_toolbar.urls)),
    ]