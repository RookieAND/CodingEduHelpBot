from custom import EmbedMessage, SelectClassView
from nextcord.ext import commands


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = EmbedMessage()

    @commands.command(name="lesson")
    async def lesson(self, ctx, *args):
        if not args:
            await ctx.send(embed=self.embed.command())
            return
        elif len(args) == 1:
            if args[0] == "introduce":
                await ctx.send(f"{ctx.author.mention} 님, 코딩 교육 강사인 저에 대한 소개를 하겠습니다.", embed=self.embed.introduce())
                return
            elif args[0] == "question":
                await ctx.send(f"{ctx.author.mention} 님! 코딩 교육 디스코드 서버에 오신 것을 환영해요!", embed=self.embed.welcome())
                return
            elif args[0] == "select":
                view = SelectClassView()
                await ctx.send(
                        f"{ctx.author.mention} 님! 하단의 항목 중에서 수강한 과목을 눌러주세요!",
                        embed=self.embed.select_lang(None), view=view, delete_after=10.0
                    )
                await view.wait()
                if view.lang is None:
                    await ctx.send(f"{ctx.author.mention} 님! 시간이 초과되어 과목 선택이 취소되었습니다!", delete_after=3.0)
                else:
                    ctx.author.get_role(role_id=view.role[view.lang])
        else:
            await ctx.send(embed=self.embed.command())


def setup(bot):
    bot.add_cog(BotCommands(bot))
