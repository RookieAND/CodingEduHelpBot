from custom import EmbedMessage, SelectClassView
from nextcord.ext import commands
from timetable import Timetable

timetable = Timetable()


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
            if args[0] == "author":
                await ctx.send(f"{ctx.author.mention} 님, 지금부터 선생님에 대한 소개를 하겠습니다.", embed=self.embed.introduce())
                return
            elif args[0] == "question":
                await ctx.send(f"{ctx.author.mention} 님! 선생님에게 질문할 내용이 있으신가 보군요?", embed=self.embed.question())
                return
            elif args[0] == "select":
                view = SelectClassView()
                await ctx.send(
                        f"{ctx.author.mention} 님! 아래 버튼들 중에서 수강한 과목을 눌러주세요!",
                        embed=self.embed.select_lang_default(), view=view, delete_after=10.0
                    )
                await view.wait()
                if view.lang is None:
                    await ctx.send(
                        f"{ctx.author.mention} 님! 시간이 지나 과목 선택이 취소 되었습니다!",
                        embed=self.embed.select_lang_failed(), delete_after=5.0)
                else:
                    guild = ctx.guild
                    role = guild.get_role(view.role[view.lang])
                    await guild.get_member(ctx.author.id).add_roles(role)
        else:
            await ctx.send(embed=self.embed.command())

    @commands.command(name="timetable")
    async def timetable(self, ctx, *args):
        if not args:
            await ctx.send(embed=self.embed.command())
            return
        elif len(args) == 1:
            weekday = {'Mon': "월요일", 'Tue': "화요일", 'Wed': "수요일", 'Thu': "목요일", 'Fri': "금요일"}
            if args[0] in weekday:
                day = args[0]
                class_info = timetable.get_day_class(day)
                await ctx.send(
                    f"{ctx.author.mention} 님, **{weekday[day]}**의 시간표를 가져왔어요! 한번 봐주세요!",
                    embed=self.embed.timetable_daily(weekday[day], class_info)
                )
                return
            else:
                await ctx.send(f"{ctx.author.mention} 님, 요일은 영어로만 입력이 가능해요!.", embed=self.embed.timetable_daily_failed())
        else:
            await ctx.send(embed=self.embed.command())


def setup(bot):
    bot.add_cog(BotCommands(bot))
