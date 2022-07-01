from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction
from disnake import Message as Msg
from disnake import TextChannel
from disnake.ext.commands import has_permissions, slash_command

from core.cog import GeneralCog
from utils.auto_completer import choose_mapping_generater
from utils.message import TargetMessage

if TYPE_CHECKING:
    from core.bot import LuxRay


class Message(GeneralCog):
    # Internal logic
    @staticmethod
    async def delete_system_message(channel: TextChannel):
        async for message in channel.history(limit=3):
            if message.is_system():
                await message.delete()
                break

    # Commands
    @slash_command(dm_permission=False, name="keyword-reply")
    async def keyword_reply(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str = None,
    ):
        if not keyword:
            server = await self.get_server(inter.guild_id)
            keywords = server.message.keywords
            return (
                await inter.send(
                    str(keywords)[1:-1].replace("'", "`").replace(", ", ",\n")
                )
                if keywords
                else await inter.send("No keywords have been set for this server")
            )
        await inter.send(keyword)

    ## message
    @slash_command(dm_permission=False)
    @has_permissions(manage_messages=True)
    async def message(self, inter: ApplicationCommandInteraction):
        pass

    @message.sub_command()
    async def pin(self, inter: ApplicationCommandInteraction):
        server = await self.get_server(inter.guild_id)

        async def pin(message: Msg):
            await message.pin(
                reason=server.translate(
                    "User `{user_name_with_id}` use command `{command_name}`"
                ).format(
                    user_name_with_id=f"{inter.author.name}(ID: {inter.author.id})",
                    command_name=inter.application_command.name,
                )
            )
            await self.delete_system_message(message.channel)

        async with TargetMessage(inter) as message:
            if message.pinned:
                return await server.send_ephemeral(inter, "Message pinned")
            await pin(message)
            await server.send_ephemeral(inter, "Successful pinning message")

    @message.sub_command()
    async def unpin(self, inter: ApplicationCommandInteraction):
        server = await self.get_server(inter.guild_id)

        async def unpin(message: Msg):
            await message.unpin(
                reason=server.translate(
                    "User `{user_name_with_id}` use command `{command_name}`"
                ).format(
                    user_name_with_id=f"{inter.author.name}(ID: {inter.author.id})",
                    command_name=inter.application_command.name,
                )
            )
            await self.delete_system_message(message.channel)

        async with TargetMessage(inter) as message:
            if not message.pinned:
                return await server.send_ephemeral(inter, "Message not pinned")
            await unpin(message)
            await server.send_ephemeral(inter, "Successful unpinning message")

    @message.sub_command()
    async def purge(self, inter: ApplicationCommandInteraction, amount: int = 1):
        await inter.channel.purge(limit=amount + 1)
        server = await self.get_server(inter.guild_id)
        await server.send_ephemeral(
            "`{amount}` message(s) deleted", message_format={"amount": amount}
        )

    # Auto-complete
    @keyword_reply.autocomplete("keyword")
    async def reply_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords: dict[str, str] = server.message.keywords
        return choose_mapping_generater(keywords, user_input)


def setup(bot: "LuxRay"):
    bot.add_cog(Message(bot))
