from discord import HTTPException, Message, TextChannel
from discord.ext.commands import Bot
from exceptions import InvalidChannelID, InvalidMessageID, InvalidMessageLink


async def parse_message_link(bot: Bot, message_link: str):
	"""
	Parameter
	---------
	message_link: `str`
		a link that contain `https://discord.com/channels/`
	
	Raise
	-----
	InvalidMessageLink: when `message_link` is incomplete
	InvalidChannelID: when chennel doesn't exist
	InvalidMessageID: when channel is not readable for bot or message doesn't exist
	
	Return
	------
	Message(discord.message.Message)
	"""
	link_prefix = "https://discord.com/channels/"
	
	if link_prefix in message_link:
		try:
			channel_id, message_id = message_link.removeprefix("https://discord.com/channels/").split("/")[1:]
			channel: TextChannel = bot.get_channel(int(channel_id))
			message: Message = await channel.fetch_message(int(message_id))
			return message
		except ValueError:
			# `message_link` is incomplete
			raise InvalidMessageLink(message_link)
		except AttributeError:
			# 'NoneType' object has no 'fetch_message' attribute -> channel doesn't exist
			raise InvalidChannelID(channel_id)
		except HTTPException:
			# channel not readable or message doesn't exist
			raise InvalidMessageID(message_id)
	else:
		raise InvalidMessageLink(message_link)

async def get_last_exist_message(channel: TextChannel) -> Message:
	return [message async for message in channel.history(limit=1)][0]
