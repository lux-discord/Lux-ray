from disnake import ApplicationCommandInteraction, Message, TextChannel
from disnake.ext.commands import Bot

from utils.checks import has_channel_permissions


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
            _, channel_id, message_id = [
                int(item) for item in message_link.removeprefix(link_prefix).split("/")
            ]

            if not (channel := bot.get_channel(channel_id)):
                raise ValueError(f"Invalid channel ID '{channel_id}'")
            if not (message := await channel.fetch_message(message_id)):
                raise ValueError(f"Invalid message ID '{message_id}'")

            return message
        except ValueError as exc:
            # Split failure
            raise ValueError(f"Invalid message link '{message_link}'") from exc
    else:
        raise ValueError(
            f"Invalid message link '{message_link}', missing prefix '{link_prefix}'"
        )


async def get_last_exist_message(channel: TextChannel):
    messages = await channel.history(limit=1).flatten()
    return messages[0]


class TargetMessage:
    def __init__(
        self,
        inter: ApplicationCommandInteraction,
        *,
        last_message: bool = False,
        message_link: str = "",
        **perms: bool,
    ):
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
        """
        if not (last_message or message_link):
            raise ValueError(
                "One of `last_message`/`message_link` must be True/non-empty"
            )

        self.inter = inter
        self.last_message = last_message
        self.message_link = message_link
        self.perms = perms

    async def __aenter__(self) -> Message:
        if self.message_link:
            message = await resolve_message_link(self.inter.bot, self.message_link)

            if not self.perms or has_channel_permissions(
                self.inter.author, message.channel, **self.perms
            ):
                return message
        if self.last_message:
            return await get_last_exist_message(self.inter.channel)

    async def __aexit__(self, type_, value, traceback):
        pass
