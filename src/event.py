from src.embed import EmbedMessage
from nextcord.ext import commands
from timetable import Timetable


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = EmbedMessage()

    # 학생이 서버에 처음 들어왔을 때, Trial Student 역할을 지급함
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            channel.send(embed=self.embed.welcome())
            trial_role = member.guild.get_role(950362342141595678)
            member.add_roles(trial_role)

    @commands.Cog.listener()
    async def on_disconnect(self):
        Timetable.close_mysql()

def setup(bot):
    bot.add_cog(BotEvents(bot))
