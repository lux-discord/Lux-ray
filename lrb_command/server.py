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
from utils.auto_completer import choose_list_generater, lang_code_autocom

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
            return await server.send_ephemeral(
                inter,
                "Prefix of this server if `{server_prefix}`",
                message_format={"server_prefix": server_prefix},
            )

        if prefix == server_prefix:
            return await server.send_ephemeral(inter, "Prefix did not change")

        await self.update_prefix(server.PrefixData(prefix))
        await server.send_ephemeral(
            inter,
            "Successful set prefix to `{prefix}`",
            message_format={"prefix": prefix},
        )

    @config_server.sub_command()
    async def language(
        self,
        inter: ApplicationCommandInteraction,
        lang_code: str = Param(autocomplete=lang_code_autocom),
    ):
        server = await self.get_server(inter.guild_id)

        if lang_code not in GLOBAL_SUPPORT_LANGUAGE:
            return await server.send_ephemeral(
                inter,
                "Language code `{lang_code}` is not support",
                message_format={"lang_code": lang_code},
            )

        if server.lang_code == lang_code:
            return await server.send_ephemeral(inter, "Language did not change")

        await self.update_server(server.Data(lang_code=lang_code))
        server = server.update(lang_code=lang_code)
        await server.send_ephemeral(
            inter,
            "Successful set language to `{lang_code}`",
            message_format={"lang_code": lang_code},
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
        auto_roles = server.role.auto

        # List auto-roles that have been set
        if not role:
            return await server.send_ephemeral(
                inter,
                str([inter.guild.get_role(role_id).name for role_id in auto_roles])[
                    1:-1
                ].replace("'", "`")
                or server.translate("No auto-roles have been set for this server"),
            )

        if (role_id := role.id) in auto_roles:
            return await server.send_ephemeral(
                inter,
                "Role `{role_name}(ID: {role_id})` already in auto-roles",
                message_format={"role_name": role.name, "role_id": role_id},
            )

        auto_roles.append(role_id)
        await self.update_server(server.Data({"role.auto": auto_roles}))
        await server.send_ephemeral(
            inter,
            "Successful add role `{role_name}(ID: {role_id})` to auto-roles",
            message_format={"role_name": role.name, "role_id": role_id},
        )

    @auto_role.sub_command(name="remove")
    async def remove_auto_role(self, inter: ApplicationCommandInteraction, role: Role):
        server = await self.get_server(inter.guild_id)
        auto_roles = server.role.auto

        try:
            index = auto_roles.index(role_id := role.id)
        except ValueError:
            return await server.send_ephemeral(
                inter,
                "Role `{role_name}(ID: {role_id})` not in auto-roles",
                message_format={"role_name": role.name, "role_id": role_id},
            )

        auto_roles.pop(index)
        await self.update_server(server.Data({"role.auto": auto_roles}))
        await server.send_ephemeral(
            inter,
            "Successful remove role `{role_name}(ID: {role_id})` from auto-roles",
            message_format={"role_name": role.name, "role_id": role_id},
        )

    ## config-message
    @slash_command(
        default_member_permissions=Permissions(manage_guild=True, manage_messages=True),
        dm_permission=False,
        name="config-message",
    )
    async def config_message(self, inter: ApplicationCommandInteraction):
        pass

    ### keyword
    @config_message.sub_command_group()
    async def keyword(self, inter: ApplicationCommandInteraction):
        pass

    @keyword.sub_command(name="set")
    async def set_keyword(
        self, inter: ApplicationCommandInteraction, keyword: str, reply: str
    ):
        server = await self.get_server(inter.guild_id)
        await self.__set_keyword_reply(inter.guild_id, {keyword: reply})
        await server.send_ephemeral(
            inter,
            "Set reply `{reply}` for keyword `{keyword}`",
            message_format={"reply": reply, "keyword": keyword},
        )

    @keyword.sub_command(name="remove")
    async def remove_keyword(
        self,
        inter: ApplicationCommandInteraction,
        keyword: str,
    ):
        server = await self.get_server(inter.guild_id)
        await self.__del_keyword_reply(inter.guild_id, keyword)
        await server.send_ephemeral(
            inter, "Deleted keyword `{keyword}`", message_format={"keyword": keyword}
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
        await server.send_ephemeral(
            inter,
            "Set `member join message` channel to {channel}",
            message_format={"channel": channel.mention},
        )

    @set_channel.sub_command(name="member-leave-message")
    async def member_leave_message(
        self, inter: ApplicationCommandInteraction, channel: TextChannel
    ):
        server = await self.get_server(inter.guild_id)
        await self.update_server(server.Data({"channel.member_leave": channel.id}))
        await server.send_ephemeral(
            inter,
            "Set `member leave message` channel to {channel}",
            message_format={"channel": channel.mention},
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
            return await server.send_ephemeral(
                inter,
                ", ".join(requestable_category.values())
                or server.translate(
                    "No requestable category have been set for this server"
                ),
            )

        # Add specified category to requestable category
        if (category_id := category.id) not in requestable_category:
            category_name = category.name
            requestable_category[str(category_id)] = category_name
            await self.update_server(
                server.Data({"channel.requestable_category": requestable_category})
            )
            return await server.send_ephemeral(
                inter,
                "Added `{category_name}` to requestable categories",
                message_format={"category_name": category_name},
            )

        await server.send_ephemeral(
            inter,
            "`{category_name}` already in requestable categories",
            message_format={"category_name": category.name},
        )

    @requestable_category.sub_command(name="remove")
    async def remove_requestable_category(
        self, inter: ApplicationCommandInteraction, category: CategoryChannel
    ):
        server = await self.get_server(inter.guild_id)
        requestable_category = server.channel.requestable_category

        # Check if category is requestable
        if (category_id := category.id) not in requestable_category:
            return await server.send_ephemeral(
                inter,
                "`{category_name}` not in requetable categories",
                message_format={"category_name": category.name},
            )

        del requestable_category[category_id]
        await self.update_server(
            server.Data({"channel.requestable_category": requestable_category})
        )
        await server.send_ephemeral(
            inter,
            "Removed `{category_name}` from requestable categories",
            message_format={"category_name": category.name},
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
        await self.update_server(
            server.Data({"channel.category_request_process_channel": channel.id})
        )
        await server.send_ephemeral(
            inter,
            "Set `category request` process channel to {channel}",
            message_format={"channel": channel.mention},
        )

    @process.sub_command(name="channel-request")
    async def channel_request(
        self, inter: ApplicationCommandInteraction, channel: TextChannel
    ):
        server = await self.get_server(inter.guild_id)
        await self.update_server(
            server.Data({"channel.channel_request_process_channel": channel.id})
        )
        await server.send_ephemeral(
            inter,
            "Set `channel request` process channel to {channel}",
            message_format={"channel": channel.mention},
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
