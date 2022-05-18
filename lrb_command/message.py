from disnake import ApplicationCommandInteraction
from disnake import Message as Msg
from disnake import Permissions, TextChannel
from disnake.ext.commands import Context, Param, command, has_permissions, slash_command

from core.cog import GeneralCog
from utils.auto_completer import bool_autocom
from utils.message import TargetMessage


class Message(GeneralCog):
    @staticmethod
    async def delete_system_message(channel: TextChannel):
        async for message in channel.history(limit=5):
            if message.is_system():
                await message.delete()
                break

    @command()
    @has_permissions(manage_messages=True)
    async def pin(self, ctx: Context):
        await ctx.message.delete()
        server = await self.get_server(ctx.guild.id)

        async def do_pin(message: Msg):
            reason = server.translate(
                "User `{user_name_with_id}` used command `{command_name}`"
            ).format(
                user_name_with_id=f"{ctx.author.name}(ID: {ctx.author.id})",
                command_name=ctx.invoked_with,
            )

            await message.pin(reason=reason)
            await self.delete_system_message(message.channel)
            await server.send_info(ctx, "Successful pinning message")

        async with TargetMessage(ctx) as message:
            if message.pinned:
                return await server.send_warning(ctx, "Message pinned")
            await do_pin(message)

    @command()
    @has_permissions(manage_messages=True)
    async def unpin(self, ctx: Context):
        await ctx.message.delete()
        server = await self.get_server(ctx.guild.id)

        async def unpin_message(message: Msg):
            reason = server.translate(
                "User `{user_name_with_id}` used command `{command_name}`"
            ).format(
                user_name_with_id=f"{ctx.author.name}(ID: {ctx.author.id})",
                command_name=ctx.invoked_with,
            )
            await message.unpin(reason=reason)
            await self.delete_system_message(message.channel)
            await server.send_info(ctx, "Successful unpinning message")

        async with TargetMessage(ctx) as message:
            if not message.pinned:
                return await server.send_warning(ctx, "Message not pinned")
            await unpin_message(message)

    @command(aliases=["mes_link", "msg_link"])
    async def message_link(self, ctx: Context):
        async with TargetMessage(ctx) as message:
            return await ctx.send(message.jump_url)

    @command(aliases=["del_mes", "del_msg", "purge"])
    @has_permissions(manage_messages=True)
    async def delete_message(self, ctx: Context, amount: int = 1):
        await ctx.channel.purge(limit=amount + 1)
        await self.send_info(ctx, "`{amount}` message(s) deleted", amount=amount)

    # Internal logic
    async def __set_keyword_reply(self, guild_id: int, keywords: dict[str, str]):
        server = await self.get_server(guild_id)
        _keywords = server.keywords or {}
        await self.update_server(server.update(keywords=_keywords | keywords))

    async def __del_keyword_reply(self, guild_id: int, *keywords: str):
        server = await self.get_server(guild_id)
        _keywords = server.keywords or {}
        [_keywords.pop(target, None) for target in keywords]
        await self.update_server(server.update(keywords=_keywords))

    # Slash command
    async def keyword_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords: dict[str, str] = server.keywords
        return (
            keywords
            if not user_input
            else {
                words: keywords[words]
                for words in keywords
                if user_input.lower() in words
            }
        )

    # General
    @slash_command(dm_permission=False)
    async def keyword(self, inter):
        pass

    @keyword.sub_command()
    async def list_all(self, inter: ApplicationCommandInteraction):
        server = await self.get_server(inter.guild_id)
        keywords = server.keywords
        await inter.send(
            str(keywords)[1:-1].replace("'", "`").replace(", ", ",\n")
        ) if keywords else await inter.send("No keywords have been set for this server")

    @keyword.sub_command()
    async def reply(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str,
    ):
        await inter.send(keyword)

    @reply.autocomplete("keyword")
    async def reply_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords: dict[str, str] = server.keywords
        return (
            keywords
            if not user_input
            else {
                words: keywords[words]
                for words in keywords
                if user_input.lower() in words
            }
        )

    # For admin
    @slash_command(
        dm_permission=False, default_member_permissions=Permissions(administrator=True)
    )
    async def keyword_edit(self, inter):
        pass

    @keyword_edit.sub_command()
    async def set_reply(
        self, inter: ApplicationCommandInteraction, keyword: str, reply: str
    ):
        await self.__set_keyword_reply(inter.guild_id, {keyword: reply})
        await inter.send(f"Set reply `{reply}` for keyword `{keyword}`")

    @keyword_edit.sub_command()
    async def del_reply(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str,
    ):
        await self.__del_keyword_reply(inter.guild_id, keyword)
        await inter.send(f"Deleted keyword `{keyword}`")

    @del_reply.autocomplete("keyword")
    async def del_reply_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords = list(server.keywords.keys())
        return (
            keywords
            if not user_input
            else [words for words in keywords if user_input.lower() in words]
        )

    @slash_command(
        dm_permission=False, default_member_permissions=Permissions(administrator=True)
    )
    async def listen_message(
        self,
        inter: ApplicationCommandInteraction,
        choose: str = Param(autocomplete=bool_autocom),
    ):
        choose_to_bool = {"True": True, "False": False}

        if choose not in choose_to_bool:
            return inter.send(f"Invalid value: `{choose}`")

        server = await self.get_server(inter.guild_id)

        if not server.listen_message == (choose := choose_to_bool[choose]):
            await self.update_server(server.update(listen_message=choose))
            return await inter.send(f"Set listen message to {choose}")
        await inter.send("Value not change")


def setup(bot):
    bot.add_cog(Message(bot))
