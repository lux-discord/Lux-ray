from disnake import ApplicationCommandInteraction
from disnake import Message as Msg
from disnake import Permissions, TextChannel
from disnake.ext.commands import Param, slash_command

from core.cog import GeneralCog
from utils.auto_completer import (
    bool_autocom,
    choose_list_generater,
    choose_mapping_generater,
)
from utils.converter import STR_TO_BOOL
from utils.message import TargetMessageInter


class Message(GeneralCog):
    # Internal logic
    @staticmethod
    async def delete_system_message(channel: TextChannel):
        async for message in channel.history(limit=3):
            if message.is_system():
                await message.delete()
                break

    async def __set_keyword_reply(self, guild_id: int, keywords: dict[str, str]):
        server = await self.get_server(guild_id)
        _keywords = server.keywords or {}
        await self.update_server(server.update(keywords=_keywords | keywords))

    async def __del_keyword_reply(self, guild_id: int, *keywords: str):
        server = await self.get_server(guild_id)
        _keywords = server.keywords or {}
        [_keywords.pop(target, None) for target in keywords]
        await self.update_server(server.update(keywords=_keywords))

    # General command
    @slash_command(dm_permission=False)
    async def keyword(self, inter):
        pass

    @keyword.sub_command()
    async def reply(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str = None,
    ):
        if not keyword:
            server = await self.get_server(inter.guild_id)
            keywords = server.keywords
            return (
                await inter.send(
                    str(keywords)[1:-1].replace("'", "`").replace(", ", ",\n")
                )
                if keywords
                else await inter.send("No keywords have been set for this server")
            )
        await inter.send(keyword)

    @reply.autocomplete("keyword")
    async def reply_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords: dict[str, str] = server.keywords
        return choose_mapping_generater(keywords, user_input)

    # Manage messages
    ## General
    @slash_command(
        default_member_permissions=Permissions(manage_messages=True), name="pin"
    )
    async def pin(self, inter: ApplicationCommandInteraction):
        server = await self.get_server(inter.guild_id)

        async def pin(message: Msg):
            await message.pin(
                reason=server.translate(
                    "User `{user_name_with_id}` used command `{command_name}`"
                ).format(
                    user_name_with_id=f"{inter.author.name}(ID: {inter.author.id})",
                    command_name=inter.application_command.name,
                )
            )
            await self.delete_system_message(message.channel)

        async with TargetMessageInter(inter) as message:
            if message.pinned:
                return await server.send_warning(inter, "Message pinned")
            await pin(message)
            await server.send_info(inter, "Successful pinning message")

    @slash_command(
        default_member_permissions=Permissions(manage_messages=True), name="unpin"
    )
    async def unpin(self, inter: ApplicationCommandInteraction):
        server = await self.get_server(inter.guild_id)

        async def unpin(message: Msg):
            await message.unpin(
                reason=server.translate(
                    "User `{user_name_with_id}` used command `{command_name}`"
                ).format(
                    user_name_with_id=f"{inter.author.name}(ID: {inter.author.id})",
                    command_name=inter.application_command.name,
                )
            )
            await self.delete_system_message(message.channel)

        async with TargetMessageInter(inter) as message:
            if not message.pinned:
                return await server.send_warning(inter, "Message not pinned")
            await unpin(message)
            await server.send_info(inter, "Successful unpinning message")

    @slash_command(
        default_member_permissions=Permissions(manage_messages=True),
        name="delete_message",
    )
    async def delete_message(
        self, inter: ApplicationCommandInteraction, amount: int = 1
    ):
        await inter.channel.purge(limit=amount + 1)
        await self.send_info(inter, "`{amount}` message(s) deleted", amount=amount)

    ## Keyword
    @slash_command(
        dm_permission=False,
        default_member_permissions=Permissions(manage_messages=True),
    )
    async def keyword_edit(self, inter):
        pass

    @keyword_edit.sub_command(name="set")
    async def set_reply(
        self, inter: ApplicationCommandInteraction, keyword: str, reply: str
    ):
        await self.__set_keyword_reply(inter.guild_id, {keyword: reply})
        await inter.send(f"Set reply `{reply}` for keyword `{keyword}`")

    @keyword_edit.sub_command(name="remove")
    async def remove_reply(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str,
    ):
        await self.__del_keyword_reply(inter.guild_id, keyword)
        await inter.send(f"Deleted keyword `{keyword}`")

    @remove_reply.autocomplete("keyword")
    async def remove_reply_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords = list(server.keywords.keys())
        return choose_list_generater(keywords, user_input)

    @slash_command(
        dm_permission=False, default_member_permissions=Permissions(administrator=True)
    )
    async def listen_message(
        self,
        inter: ApplicationCommandInteraction,
        choose: str = Param(autocomplete=bool_autocom),
    ):
        if choose not in STR_TO_BOOL:
            return inter.send(f"Invalid value: `{choose}`")

        server = await self.get_server(inter.guild_id)
        bool_choose = STR_TO_BOOL[choose]

        if server.listen_message != bool_choose:
            await self.update_server(server.update(listen_message=bool_choose))
            return await inter.send(f"Set listen message to {choose}")
        await inter.send("Value not change")


def setup(bot):
    bot.add_cog(Message(bot))
