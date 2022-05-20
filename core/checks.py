from disnake import Permissions, TextChannel
from disnake.ext.commands import MissingPermissions

from utils.type_hint import Author


def has_channel_permissions(author: Author, channel: TextChannel, **perms: bool):
    invalid = set(perms) - set(Permissions.VALID_FLAGS)

    if invalid:
        raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")

    permissions = channel.permissions_for(author)
    missing = [
        perm for perm, value in perms.items() if getattr(permissions, perm) != value
    ]

    if not missing:
        return True

    raise MissingPermissions(missing)
