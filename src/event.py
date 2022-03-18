from src.custom import EmbedMessage
from nextcord.ext import commands


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = EmbedMessage()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            channel.send(embed=self.embed.welcome())


def setup(bot):
    bot.add_cog(BotEvents(bot))
