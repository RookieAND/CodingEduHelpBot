import discord, embed
from discord.ext import commands

# 봇의 기본 설정을 작성하는 섹션
intents = discord.Intents.default()
intents.members = True

bot_description = '''
코딩교육 강의에 사용하기 위한 테스트 봇입니다.
이 디스코드 봇은 Python 으로 개발되었습니다.
'''
bot_activity = discord.Game(name='코딩 교육 강의')
bot = commands.Bot(
    command_prefix='!', help_command=None, description=bot_description, activity=bot_activity, intents=intents
)

embedMessage = embed.EmbedMessage()


# 봇의 이벤트 관련 핸들링을 진행하는 섹션
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
        channel.send(embed=embedMessage.welcome_message())


@bot.command()
async def lesson(ctx, *args):
    if not args:
        await ctx.send(embed=embedMessage.notice_message())
        return
    elif args[0] == "introduce" and len(args) > 0:
        await ctx.send(f"{ctx.author.mention} 코딩 교육 강사인 저에 대한 소개를 하겠습니다.", embed=embedMessage.intro_message())
        return
    elif args[0] == "test" and len(args) > 0:
        await ctx.send(f"{ctx.author.mention} 님!, 코딩 교육 디스코드 서버에 오신 것을 환영해요!", embed=embedMessage.welcome_message())
        return
    else:
        await ctx.send(embed=embedMessage.notice_message())


token = 'ODcwNjUxNTU0ODg0MTA4Mjg4.YQP3cg.sEFJ3J3AUjD54Q7d9QCMUSZBDto'
bot.run(token)
