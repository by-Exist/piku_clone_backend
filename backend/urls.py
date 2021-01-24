from accountapp.views import UserViewSet
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_nested import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from pikuapp.views import (
    CommentReportViewSet,
    CommentViewSet,
    MediaReportViewSet,
    MediaViewSet,
    WorldcupViewSet,
)
import debug_toolbar


router = routers.DefaultRouter()

router.register("users", UserViewSet)
router.register("worldcups", WorldcupViewSet)
media_router = routers.NestedSimpleRouter(router, "worldcups", lookup="worldcup")
media_router.register("medias", MediaViewSet, basename="media")
comment_router = routers.NestedSimpleRouter(router, "worldcups", lookup="worldcup")
comment_router.register("comments", CommentViewSet, basename="comment")

router.register("reports/medias", MediaReportViewSet)
router.register("reports/comments", CommentReportViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(media_router.urls)),
    path("api/", include(comment_router.urls)),
    path("api/token/", obtain_jwt_token),
    path("api/token/refresh/", refresh_jwt_token),
    path("api/token/verify/", verify_jwt_token),
    path("admin/", admin.site.urls),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        # debug toolbar
        path("__debug__/", include(debug_toolbar.urls)),
        # rest
        path("api-auth/", include("rest_framework.urls")),
        # swagger
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]