import json

from embed import EmbedMessage, SelectClassView
from nextcord.ext import commands
from nextcord import Member
from timetable import Timetable


class CommandLesson(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = EmbedMessage()

    @commands.group(name="lesson", aliases=['class'])
    async def lesson(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                f"{ctx.author.mention} 님! 명령어를 잘못 입력하신 것 같습니다!",
                embed=self.embed.command()
            )

    @lesson.command(name="author")
    async def lesson_author(self, ctx: commands.Context):
        await ctx.send(f"{ctx.author.mention} 님, 지금부터 선생님에 대한 소개를 하겠습니다.", embed=self.embed.introduce())

    @lesson.command(name="question")
    async def lesson_author(self, ctx: commands.Context):
        await ctx.send(f"{ctx.author.mention} 님! 선생님에게 질문할 내용이 있으신가 보군요?", embed=self.embed.question())

    @lesson.command(name="select")
    async def lesson_select(self, ctx: commands.Context):
        view = SelectClassView()
        await ctx.send(
            f"{ctx.author.mention} 님! 아래 버튼들 중에서 수강한 과목을 눌러주세요!",
            embed=self.embed.select_lang_default(), view=view, delete_after=10.0
        )
        await view.wait()
        if view.lang is None:
            await ctx.send(
                f"{ctx.author.mention} 님! 시간이 지나 과목 선택이 취소 되었습니다!",
                embed=self.embed.select_lang_failed(), delete_after=10.0)
        else:
            guild = ctx.guild
            role = guild.get_role(view.role[view.lang])
            await guild.get_member(ctx.author.id).add_roles(role)


class CommandTimetable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = EmbedMessage()
        self.timetable = Timetable()
        self.weekday = {'Mon': "월요일", 'Tue': "화요일", 'Wed': "수요일", 'Thu': "목요일", 'Fri': "금요일"}
        with open('../data/config.json') as f:
            config = json.load(f)
            self.role = {config['PYTHON_ROLE_ID']: "Python", config['MAKECODE_ROLE_ID']: "MakeCode"}

    @commands.group(name="timetable", aliases=['tt', 'ttable'])
    async def timetable(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                f"{ctx.author.mention} 님! 명령어를 잘못 입력하신 것 같습니다!",
                embed=self.embed.command()
            )

    @timetable.command(name="show", aliases=['s'])
    async def timetable_show(self, ctx: commands.Context, day: str = None):
        if day is None:
            await ctx.send(
                f"{ctx.author.mention} 님, 시간표를 열람할 요일을 입력해주세요!", embed=self.embed.timetable_daily_failed()
            )
        elif day in self.weekday:
            class_info = self.timetable.get_day_class(day)
            if class_info is not None:
                await ctx.send(
                    f"{ctx.author.mention} 님, **{self.weekday[day]}**의 시간표를 가져왔어요! 한번 봐주세요!",
                    embed=self.embed.timetable_daily(class_info)
                )
            else:
                await ctx.send(
                    f"{ctx.author.mention} 님, 해당 요일에는 수업이 존재하지 않아요!", embed=self.embed.timetable_daily_empty()
                )
        else:
            await ctx.send(
                f"{ctx.author.mention} 님, 요일은 영어로만 입력이 가능해요!", embed=self.embed.timetable_daily_failed()
            )

    # 시간표 추가 명령어 : [timetable add <요일> <시간> <학생>]
    @timetable.command(name="add", aliases=['a'])
    @commands.has_permissions(kick_members=True)
    async def timetable_add(self, ctx: commands.Context, day: str = None, time: int = None, student: Member = None):
        if day is None or day not in self.weekday:
            reason = "day"
        else:
            if time is None or not (0 <= time <= 23):
                reason = "time"
            else:
                if student is None:
                    reason = "student"
                else:
                    course_info = self.timetable.find_course(day, time)
                    if course_info:
                        await ctx.send(
                            f"{ctx.author.mention} 님, 해당 시간대에는 이미 다른 수업이 존재해요!",
                            embed=self.embed.timetable_modify_failed("add")
                        )
                    else:
                        # self.role 내의 role id 중에서 해당 학생이 가진 id가 있다면 이를 list에 추가함.
                        course = [role_id for role_id in self.role.keys() if student.get_role(int(role_id)) is not None][0]
                        if course:
                            self.timetable.add_student(day, time, self.role[course], student)
                            class_info = self.timetable.get_day_class(day)
                            await ctx.send(
                                f"{ctx.author.mention} 님, 성공적으로 **{student}** 학생의 수업을 추가했어요!",
                                embed=self.embed.timetable_modify(class_info, "add")
                            )
                        else:
                            await ctx.send(
                                f"{ctx.author.mention} 님, 현재 해당 학생에게 주어진 과목 역할이 없어요!",
                                embed=self.embed.timetable_add_failed("course")
                            )
                    return
        await ctx.send(
            f"{ctx.author.mention} 님, 명령어 입력을 잘못한 것 같아요!",
            embed=self.embed.timetable_add_failed(reason)
        )

    # 시간표 추가 명령어 : [timetable remove <학생>]
    @timetable.command(name="remove", aliases=['r'])
    @commands.has_permissions(kick_members=True)
    async def timetable_remove(self, ctx: commands.Context, student: Member = None):
        if student is not None:
            course_info = self.timetable.find_student(student)
            if course_info is not None:
                self.timetable.remove_student(student)
                class_info = self.timetable.get_day_class(course_info['weekday'])
                await ctx.send(
                    f"{ctx.author.mention} 님, 성공적으로 **{student.nick} 학생** 의 수업을 삭제했어요!",
                    embed=self.embed.timetable_modify(class_info, "del")
                )
            else:
                await ctx.send(
                    f"{ctx.author.mention} 님, 해당 학생은 현재 수업을 수강 중이지 않아요!",
                    embed=self.embed.timetable_modify_failed("del")
                )
            return
        await ctx.send(f"{ctx.author.mention} 님, 명령어 입력을 잘못한 것 같아요!.", embed=self.embed.timetable_add_failed('wrong'))


def setup(bot):
    bot.add_cog(CommandLesson(bot))
    bot.add_cog(CommandTimetable(bot))
