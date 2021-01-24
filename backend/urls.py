from accountapp.views import UserViewSet
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
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


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(media_router.urls)),
    path("api/", include(comment_router.urls)),
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