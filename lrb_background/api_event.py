from disnake import Member
from disnake.ext.commands.cog import Cog

from core.cog import GeneralCog


class ApiEvent(GeneralCog):
    @Cog.listener()
    async def on_connect(self):
        print("Connected to Discord")

    @Cog.listener()
    async def on_ready(self):
        print("Bot is ready")

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        server = await self.get_server(message.guild.id)

        if reply := server.keywords.get(message.content):
            await message.channel.send(reply)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        server = await self.get_server(member.guild.id)

        if auto_roles := server.role_auto:
            roles = [member.guild.get_role(role_id) for role_id in auto_roles]
            await member.add_roles(*roles)


def setup(bot):
    bot.add_cog(ApiEvent(bot))
