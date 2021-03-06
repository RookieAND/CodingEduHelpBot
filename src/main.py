import nextcord
from nextcord.ext import commands
import os


intents = nextcord.Intents.default()
intents.members = True
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="코딩 교육 강의")
bot = commands.Bot(command_prefix='!', help_command=None, activity=activity, intents=intents)

# 하위 목록으로 설정한 Bot Extension 을 로드하여 실행시킴.
bot.load_extension('event')
bot.load_extension('command')

# try-except 를 통해 token 값이 맞지 않을 경우 에러 메세지 출력
if __name__ == "__main__":
    try:
        bot.run(os.getenv('DISCORD_TOKEN'))
    except RuntimeError:
        print("알 수 없는 오류로 인해 봇이 강제로 종료되었습니다.")
    except nextcord.errors.LoginFailure:
        print("config.json 에서 기입한 Token에 해당되는 봇을 찾지 못했습니다.")
        print("사용 중인 봇의 Token 값을 다시 한번 더 확인하시고 봇을 실행하세요.")