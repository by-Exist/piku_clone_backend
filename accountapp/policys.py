from rest_access_policy import AccessPolicy
from django.contrib.auth import get_user_model


class UserViewSetPolicy(AccessPolicy):

    statements = [
        {
            "principal": ["*"],
            "action": ["create", "<safe_methods>"],
            "effect": "allow",
        },
        {
            "principal": ["authenticated"],
            "action": ["update", "partial_update", "destroy"],
            "condition": ["is_self_or_superuser"],
            "effect": "allow",
        },
    ]

    def is_superuser(self, request, view, action):
        user = request.user
        return getattr(user, "is_superuser")

    def is_self_or_superuser(self, request, view, action):
        user = request.user
        detail_user = get_user_model().objects.get(pk=view.kwargs["pk"])
        is_self = user is detail_user
        is_superuser = user.is_superuser
        return is_self or is_superuser