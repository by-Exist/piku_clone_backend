from rest_access_policy import AccessPolicy
from pikuapp.models import Image, Text, ImageComment, TextComment, Worldcup


class MediaViewSetPolicy(AccessPolicy):

    statements = [
        {
            "principal": ["*"],
            "action": ["<safe_methods>"],
            "effect": "allow",
        },
        {
            "principal": ["authenticated"],
            "action": ["create", "update", "partial_update", "destroy"],
            "condition": ["is_creator_or_superuser"],
            "effect": "allow",
        },
    ]

    def is_creator_or_superuser(self, request, view, action):
        user = request.user
        worldcup = (
            Worldcup.objects.filter(pk=view.kwargs["worldcup_pk"])
            .select_related("album")
            .first()
        )
        is_creator = worldcup.creator == user
        is_superuser = user.is_superuser
        return is_creator or is_superuser


class CommentViewSetPolicy(AccessPolicy):

    statements = [
        {
            "principal": ["*"],
            "action": ["create", "<safe_methods>"],
            "effect": "allow",
        },
        {
            "principal": ["authenticated"],
            "action": ["update", "partial_update", "destroy"],
            "condition": ["is_writer_or_superuser"],
            "effect": "allow",
        },
    ]

    def is_writer_or_superuser(self, request, view, action):
        writer = request.user
        comment = view.get_object()
        is_writer = comment.user == writer
        is_superuser = writer.is_superuser
        return is_writer or is_superuser


class WorldcupViewSetPolicy(AccessPolicy):

    statements = [
        {
            "principal": ["*"],
            "action": ["<safe_methods>"],
            "effect": "allow",
        },
        {
            "principal": ["authenticated"],
            "action": ["create"],
            "effect": "allow",
        },
        {
            "principal": ["authenticated"],
            "action": ["update", "partial_update", "destroy"],
            "condition": ["is_creator_or_superuser"],
            "effect": "allow",
        },
    ]

    def is_creator_or_superuser(self, request, view, action):
        user = request.user
        worldcup = view.get_object()
        is_creator = worldcup.creator == user
        is_superuser = user.is_superuser
        return is_creator or is_superuser
