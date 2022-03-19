from disnake import HTTPException, Message, TextChannel
from disnake.ext.commands import Bot
from disnake.ext.commands.context import Context
from exceptions import InvalidChannelID, InvalidMessageID, InvalidMessageLink, InvalidPermission

async def resolve_message_link(bot: Bot, message_link: str):
	"""
	Parameter
	---------
	message_link: `str`
		link of a message(that contain `https://discord.com/channels/`)
	
	Raise
	-----
	InvalidMessageLink: when `message_link` is incomplete(missing one or more of guild_id, channel_id, message_id) or not a link
	InvalidChannelID: when channel doesn't exist
	InvalidMessageID: when bot don't have permission read the channel or message doesn't exist
	
	Return
	------
	Message(discord.message.Message)
	"""
	link_prefix = "https://discord.com/channels/"
	
	if link_prefix in message_link:
		try:
			# Remove link_prefix -> split to guild_id, channel_id, message_id -> drop guild_id
			_, channel_id, message_id = [int(item) for item in message_link.removeprefix(link_prefix).split("/")]
			
			if not (channel := bot.get_channel(channel_id)):
				raise InvalidChannelID(channel_id)
			
			if not (message := await channel.fetch_message(message_id)):
				raise InvalidMessageID(message_id)
			
			return message
		except ValueError:
			raise InvalidMessageLink(message_link)
	else:
		raise InvalidMessageLink(message_link)

async def get_last_exist_message(channel: TextChannel) -> Message:
	return [message async for message in channel.history(limit=1)][0]

class target_message():
	def __init__(self, ctx: Context, *, message_link: str=None, **perms: bool):
		"""
		Parameter
		---------
		ctx: `Context`
			The context that command received
		message_link: `str` `[optional]`
			The link that needs to be resolved as a Message
		perms: `dict[str, bool]` `[optional]` `[for message_link]`
			The permission check of command author
		
		Raise
		-----
		InvalidMessageLink:
			when command author don't have enough permissions
		InvalidPermission: [when permission_checks]
			when permission name(key of permission_checks) is invalid
			
			check `discord.Permissions` for all avaliable permission names
		"""
		self.ctx = ctx
		self.message_link = message_link
		self.perms = perms
	
	async def __aenter__(self) -> Message:
		if self.message_link:
			message = await resolve_message_link(self.ctx.bot, self.message_link)
			
			if self.permission_checks:
				author_permsision = message.channel.permission_for(self.ctx.message.author)
				
				for permission_name, value in self.permission_checks.items():
					try:
						if getattr(author_permsision, permission_name) != value:
							raise InvalidMessageLink(self.message_link)
					except AttributeError:
						raise InvalidPermission(permission_name)
			
			return message
		if refer_mes := self.ctx.message.reference:
			return refer_mes.resolved
		return await get_last_exist_message(self.ctx.message.channel)
	
	async def __aexit__(self, type, value, traceback):
		pass
