from disnake import Permissions, TextChannel
from disnake.ext.commands import Context, MissingPermissions


def has_channel_permissions(ctx: Context, channel: TextChannel, **perms: bool):
    invalid = set(perms) - set(Permissions.VALID_FLAGS)

    if invalid:
        raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")

    permissions = channel.permissions_for(ctx.author)
    missing = [
        perm for perm, value in perms.items() if getattr(permissions, perm) != value
    ]

    if not missing:
        return True

    raise MissingPermissions(missing)
