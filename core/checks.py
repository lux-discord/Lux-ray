from disnake import Permissions
from exceptions import MissingPermissions


def has_channel_permissions(ctx, channel, **perms: bool):
	invalid = set(perms) - set(Permissions.VALID_FLAGS)
	
	if invalid:
		raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
	
	permissions = channel.permission_for(ctx.author)
	missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
	
	if not missing:
		return True
	
	raise MissingPermissions(missing)
