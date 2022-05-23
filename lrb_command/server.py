from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction, Permissions, Role
from disnake.ext.commands import Param, slash_command

from core.cog import GeneralCog
from core.language import GLOBAL_SUPPORT_LANGUAGE
from utils.auto_completer import lang_code_autocom

if TYPE_CHECKING:
    from core.bot import LuxRay


class Server(GeneralCog):
    # Config
    @slash_command(
        default_member_permissions=Permissions(manage_guild=True, manage_messages=True)
    )
    async def config(self, inter: ApplicationCommandInteraction):
        pass

    @config.sub_command()
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

    @config.sub_command()
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

    # Auto-role
    @config.sub_command_group(name="auto-role")
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


def setup(bot: "LuxRay"):
    bot.add_cog(Server(bot))
