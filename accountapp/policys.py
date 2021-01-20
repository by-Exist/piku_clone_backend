from rest_access_policy import AccessPolicy
from django.contrib.auth import get_user_model


class UserViewSetPolicy(AccessPolicy):
    statements = [
        {
            "principal": "anonymous",
            "action": ["create", "retrieve", "list"],
            "effect": "allow",
        },
        {
            "principal": "authenticated",
            "action": ["create", "list", "retrieve"],
            "effect": "allow",
        },
        {
            "principal": "authenticated",
            "action": ["update", "partial_update", "destroy"],
            "condition": "is_self_or_admin",
            "effect": "allow",
        },
    ]

    def is_superuser(self, request, view, action):
        user = request.user
        return getattr(user, "is_superuser")

    def is_self_or_admin(self, request, view, action):
        user = request.user
        detail_user = get_user_model().objects.get(pk=view.kwargs["pk"])
        result = False
        if user == detail_user:
            result = True
        if user.is_superuser:
            result = True
        return result