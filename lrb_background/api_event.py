from disnake import Member, Message
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
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        server = await self.get_server(message.guild.id)

        if server.message.listen and (reply := server.keywords.get(message.content)):
            await message.channel.send(reply)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        server = await self.get_server(member.guild.id)

        if auto_roles := server.role.auto:
            await member.add_roles(
                member.guild.get_role(role_id) for role_id in auto_roles
            )


def setup(bot):
    bot.add_cog(ApiEvent(bot))
