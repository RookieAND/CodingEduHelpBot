from src.embed import EmbedMessage
from nextcord.ext import tasks, commands
from timetable import *
from datetime import datetime
from pytz import timezone

import os


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = EmbedMessage()
        self.weekday = {'Mon': "월요일", 'Tue': "화요일", 'Wed': "수요일", 'Thu': "목요일", 'Fri': "금요일"}

    @commands.Cog.listener()
    async def on_ready(self):
        print("=" * 41)
        print("{0:^33}".format("코딩 교육 봇이 실행 중입니다."))
        print("{0:^41}".format("Created By RookieAND_"))
        print("=" * 41)
        # 수업 시작 5분 전 알림을 수행하는 작업 시작
        self.notice_course.start()
        # 봇 작동을 위해 필요한 DB Table이 있는지를 체크
        check_table_exist()

    # 학생이 서버에 처음 들어올 때, Trial Student 역할을 지급함
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            channel.send(embed=self.embed.welcome())
            trial_role = member.guild.get_role(950362342141595678)
            member.add_roles(trial_role)

    @tasks.loop(seconds=60.0)
    async def notice_course(self):

        # 대한민국 서울 (UTC - 9) 시간으로 현재 시간을 로드함
        now = datetime.now(timezone('Asia/Seoul'))
        weekday = now.strftime("%a")  # 현재 시간에서 요일에 대한 정보를 로드함 (%a : Mon, Tue... , Sat, Sun)
        class_info = find_course(weekday, now.hour + 1)

        # 현재 요일 시간에 수업 정보가 있는지 먼저 확인하고, 정보가 있다면 메세지를 출력시킴
        if class_info:
            if class_info['time'] == now.hour + 1 and now.minute == 55:
                guild = self.bot.get_guild(946376880595021854)
                channel = guild.get_channel(int(os.getenv('NOTICE_CHANNEL_ID')))
                student = guild.get_member(int(class_info['discordID']))
                await channel.send(
                    f"{student.mention} 님! 곧 {class_info['time']}시에 수업이 시작하니 미리 준비를 마쳐주세요!",
                    embed=self.embed.notice(self.weekday[weekday], now.hour + 1, now.strftime("%Y년 %m월 %d일 %H시 %M분"))
                )


def setup(bot):
    bot.add_cog(BotEvents(bot))
