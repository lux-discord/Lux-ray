from typing import TYPE_CHECKING

from disnake import (
    ApplicationCommandInteraction,
    CategoryChannel,
    Permissions,
    Role,
    TextChannel,
)
from disnake.ext.commands import Param, slash_command

from core.cog import GeneralCog
from core.language import GLOBAL_SUPPORT_LANGUAGE
from utils.auto_completer import bool_autocom, choose_list_generater, lang_code_autocom
from utils.converter import STR_TO_BOOL

if TYPE_CHECKING:
    from core.bot import LuxRay


class Server(GeneralCog):
    # Internal logic
    async def __set_keyword_reply(self, guild_id: int, keywords: dict[str, str]):
        server = await self.get_server(guild_id)
        _keywords = server.message.keywords or {}
        await self.update_server(
            server.Data({"message.keywords": _keywords | keywords})
        )

    async def __del_keyword_reply(self, guild_id: int, *keywords: str):
        server = await self.get_server(guild_id)
        _keywords = server.message.keywords or {}
        [_keywords.pop(target, None) for target in keywords]
        await self.update_server(server.Data({"message.keywords": _keywords}))

    # Commands
    ## config-server
    @slash_command(
        default_member_permissions=Permissions(manage_guild=True),
        dm_permission=False,
        name="config-server",
    )
    async def config_server(self, inter: ApplicationCommandInteraction):
        pass

    @config_server.sub_command()
    async def prefix(self, inter: ApplicationCommandInteraction, prefix: str = None):
        server = await self.get_server(inter.guild_id)
        server_prefix = await self.bot.db.find_prefix(inter.guild_id)

        if not prefix:
            return await inter.send(
                f"Prefix of this server if `{server_prefix}`",
                ephemeral=True,
            )
        if prefix == server_prefix:
            return await server.send(
                inter,
                "Prefix did not change",
                ephemeral=True,
            )

        await self.update_prefix(server.PrefixData(prefix))
        await server.send(
            inter,
            "Successful set prefix to `{prefix}`",
            message_format={"prefix": prefix},
            ephemeral=True,
        )

    @config_server.sub_command()
    async def language(
        self,
        inter: ApplicationCommandInteraction,
        lang_code: str = Param(autocomplete=lang_code_autocom),
    ):
        server = await self.get_server(inter.guild_id)

        if lang_code not in GLOBAL_SUPPORT_LANGUAGE:
            return await server.send(
                inter,
                "Language code `{lang_code}` is not support",
                message_format={"lang_code": lang_code},
                ephemeral=True,
            )
        if server.lang_code == lang_code:
            return await server.send(
                inter,
                "Language did not change",
                ephemeral=True,
            )

        await self.update_server(server.Data(lang_code=lang_code))
        await server.send(
            inter,
            "Successful set language to `{lang_code}`",
            message_format={"lang_code": lang_code},
            ephemeral=True,
        )

    ## config-role
    @slash_command(
        default_member_permissions=Permissions(manage_guild=True, manage_roles=True),
        dm_permission=False,
        name="config-role",
    )
    async def config_role(self, inter: ApplicationCommandInteraction):
        pass

    @config_role.sub_command_group(name="auto")
    async def auto_role(self, inter):
        pass

    @auto_role.sub_command(name="add")
    async def add_auto_role(
        self,
        inter: ApplicationCommandInteraction,
        role: Role = None,
    ):
        server = await self.get_server(inter.guild_id)
        auto_roles = server.role.auto or []

        if not role:
            return await inter.send(
                str([inter.guild.get_role(role_id).name for role_id in auto_roles])[
                    1:-1
                ].replace("'", "`")
                or "No auto-roles have been set for this server",
                ephemeral=True,
            )
        if (role_id := role.id) in auto_roles:
            return await inter.send(
                f"Role `{role.name}(ID: {role_id})` Already in auto-roles",
                ephemeral=True,
            )

        auto_roles.append(role_id)
        await self.update_server(server.Data({"role.auto": auto_roles}))
        await inter.send(
            f"Successful add role `{role.name}(ID: {role_id})` to auto-roles",
            ephemeral=True,
        )

    @auto_role.sub_command(name="remove")
    async def remove_auto_role(self, inter: ApplicationCommandInteraction, role: Role):
        server = await self.get_server(inter.guild_id)
        auto_roles = server.role_auto or []

        try:
            index = auto_roles.index(role_id := role.id)
        except ValueError:
            return await inter.send(
                f"Role `{role.name}(ID: {role_id})` not in auto-roles",
                ephemeral=True,
            )

        auto_roles.pop(index)
        await self.update_server(server.Data({"role.auto": auto_roles}))
        await inter.send(
            f"Successful remove role `{role.name}(ID: {role_id})` from auto-roles",
            ephemeral=True,
        )

    ## config-message
    @slash_command(
        default_member_permissions=Permissions(manage_guild=True, manage_messages=True),
        dm_permission=False,
        name="config-message",
    )
    async def config_message(self, inter: ApplicationCommandInteraction):
        pass

    @config_message.sub_command()
    async def listen(
        self,
        inter: ApplicationCommandInteraction,
        choose: str = Param(autocomplete=bool_autocom),
    ):
        if choose not in STR_TO_BOOL:
            return inter.send(
                f"Invalid value: `{choose}`",
                ephemeral=True,
            )

        server = await self.get_server(inter.guild_id)
        bool_choose = STR_TO_BOOL[choose]

        if server.message.listen != bool_choose:
            await self.update_server(server.Data({"message.listen": bool_choose}))
            return await inter.send(
                f"Set listen message to {choose}",
                ephemeral=True,
            )
        await inter.send(
            "Value not change",
            ephemeral=True,
        )

    ### keyword
    @config_message.sub_command_group()
    async def keyword(self, inter: ApplicationCommandInteraction):
        pass

    @keyword.sub_command(name="set")
    async def set_keyword(
        self, inter: ApplicationCommandInteraction, keyword: str, reply: str
    ):
        await self.__set_keyword_reply(inter.guild_id, {keyword: reply})
        await inter.send(
            f"Set reply `{reply}` for keyword `{keyword}`",
            ephemeral=True,
        )

    @keyword.sub_command(name="remove")
    async def remove_keyword(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str,
    ):
        await self.__del_keyword_reply(inter.guild_id, keyword)
        await inter.send(
            f"Deleted keyword `{keyword}`",
            ephemeral=True,
        )

    ## config-channel
    @slash_command(
        default_member_permissions=Permissions(manage_guild=True, manage_channels=True),
        dm_permission=False,
        name="config-channel",
    )
    async def config_channel(self, inter: ApplicationCommandInteraction):
        pass

    ### set-channel
    @config_channel.sub_command_group(name="set")
    async def set_channel(self, inter: ApplicationCommandInteraction):
        pass

    @set_channel.sub_command(name="member-join-message")
    async def member_join_message(
        self, inter: ApplicationCommandInteraction, channel: TextChannel
    ):
        server = await self.get_server(inter.guild_id)
        await self.update_server(server.Data({"channel.member_join": channel.id}))
        await inter.send(
            f"Set `member join message` channel to {channel.mention}", ephemeral=True
        )

    @set_channel.sub_command(name="member-leave-message")
    async def member_leave_message(
        self, inter: ApplicationCommandInteraction, channel: TextChannel
    ):
        server = await self.get_server(inter.guild_id)
        await self.update_server(server.Data({"channel.member_leave": channel.id}))
        await inter.send(
            f"Set `member leave message` channel to {channel.mention}", ephemeral=True
        )

    ### requestable
    @config_channel.sub_command_group(name="requestable-category")
    async def requestable_category(self, inter: ApplicationCommandInteraction):
        pass

    @requestable_category.sub_command(name="add")
    async def add_requestable_category(
        self, inter: ApplicationCommandInteraction, category: CategoryChannel = None
    ):
        server = await self.get_server(inter.guild_id)
        requestable_category = server.channel.requestable_category

        # List added category
        if not category:
            return await inter.send(
                ", ".join(requestable_category.values())
                or "No requestable category have been set for this server",
                ephemeral=True,
            )

        # Add specified category to requestable category
        if (category_id := category.id) not in requestable_category:
            category_name = category.name
            requestable_category[str(category_id)] = category_name
            await self.update_server(
                server.Data({"channel.requestable_category": requestable_category})
            )
            return await inter.send(
                f"Added `{category_name}` to requestable categories", ephemeral=True
            )

        await inter.send(
            f"`{category.name}` already in requestable categories", ephemeral=True
        )

    @requestable_category.sub_command(name="remove")
    async def remove_requestable_category(
        self, inter: ApplicationCommandInteraction, category: CategoryChannel
    ):
        server = await self.get_server(inter.guild_id)
        requestable_category = server.channel.requestable_category

        # Check if category is requestable
        if (category_id := category.id) not in requestable_category:
            return await inter.send(
                f"`{category.name}` not in requetable categories", ephemeral=True
            )

        del requestable_category[category_id]
        await self.update_server(
            server.Data({"channel.requestable_category": requestable_category})
        )
        await inter.send(
            f"Removed `{category.name}` from requestable categories", ephemeral=True
        )

    ### process
    @config_channel.sub_command_group()
    async def process(self, inter: ApplicationCommandInteraction):
        pass

    @process.sub_command(name="category-request")
    async def category_request(
        self, inter: ApplicationCommandInteraction, channel: TextChannel
    ):
        server = await self.get_server(inter.guild_id)
        await self.update_server(server.Data({"channel.category_request": channel.id}))
        await inter.send(
            f"Set `category request` channel to {channel.mention}", ephemeral=True
        )

    @process.sub_command(name="channel-request")
    async def channel_request(
        self, inter: ApplicationCommandInteraction, channel: TextChannel
    ):
        server = await self.get_server(inter.guild_id)
        await self.update_server(server.Data({"channel.channel_request": channel.id}))
        await inter.send(
            f"Set `channel request` channel to {channel.mention}", ephemeral=True
        )

    # Auto-complete
    @remove_keyword.autocomplete("keyword")
    async def remove_keyword_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        keywords = list(server.message.keywords.keys())
        return choose_list_generater(keywords, user_input)


def setup(bot: "LuxRay"):
    bot.add_cog(Server(bot))
