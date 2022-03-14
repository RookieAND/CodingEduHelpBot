from custom import EmbedMessage, SelectClassView
import nextcord
from nextcord.ext import commands


# 봇의 기본 설정을 작성하는 섹션
class CodingBot:
    def __init__(self):
        self.intents = nextcord.Intents.default()
        self.intents.members = True
        self.bot_activity = nextcord.Game(name='코딩 교육 강의')
        self.cmd_prefix = '!'
        self.token = 'ODcwNjUxNTU0ODg0MTA4Mjg4.YQP3cg.hhMrNP45jCruAG8Ha8Sy51ZYdI8'


cdBot = CodingBot()
embed = EmbedMessage()
bot = commands.Bot(
    command_prefix=cdBot.cmd_prefix, help_command=None,
    activity=cdBot.bot_activity, intents=cdBot.intents
)


# 봇의 이벤트를 진행하는 섹션
@bot.event
async def on_ready():
    print("=" * 41)
    print("{0:^33}".format("코딩 교육 봇이 실행 중입니다."))
    print("{0:^41}".format("Created By RookieAND_"))
    print("=" * 41)


@bot.command()
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        channel.send(embed=embed.welcome())


@bot.command()
async def lesson(ctx, *args):
    if not args:
        await ctx.send(embed=embed.command())
        return
    elif len(args) == 1:
        if args[0] == "introduce":
            await ctx.send(f"{ctx.author.mention} 님, 코딩 교육 강사인 저에 대한 소개를 하겠습니다.", embed=embed.introduce())
            return
        elif args[0] == "question":
            await ctx.send(f"{ctx.author.mention} 님! 코딩 교육 디스코드 서버에 오신 것을 환영해요!", embed=embed.welcome())
            return
        elif args[0] == "select":
            view = SelectClassView()
            await ctx.send(
                    f"{ctx.author.mention} 님! 하단의 항목 중에서 수강한 과목을 눌러주세요!",
                    embed=embed.select_lang(None), view=view, delete_after=10.0
                )
            # 해당 View의 Interaction 이 진행되지 전까지 실행을 기다림
            await view.wait()
            # 만약 시간 내에 역할을 선택하지 않았다면, 선택이 취소되었다는 안내 메세지 출력
            if view.lang is None:
                await ctx.send(f"{ctx.author.mention} 님! 시간이 초과되어 과목 선택이 취소되었습니다!", delete_after=3.0)
            # 그렇지 않을 경우, 성공적으로 역할이 배정되었다는 메세지를 출력시킴.
            else:
                ctx.author.get_role(role_id=view.role[view.lang])
    else:
        await ctx.send(embed=embed.command())

bot.run(cdBot.token)
