import os

import nextcord
from nextcord.ui import View

'''
    Embed 의 to_dict() 을 이용해 기본 값을 dict 형태로 작성하고 이를 변경하는 식으로 사용
    footer, thumbnail, color, author 의 경우 거의 모든 embed 가 같은 값을 공유할 예정.
    
    모든 EmbedMessage의 리턴 값은 nextcord.Embed.from_dict(self.embed) 으로 진행
    단, field 값을 추가해야 할 경우 먼저 Embed 객체로 변환하여 add_field 함수를 진행함
'''


class EmbedMessage:
    def __init__(self):
        image_url = 'https://cdn-icons-png.flaticon.com/512/4712/4712139.png'
        self.embed = {
            'footer': {'text': 'Made by RookieAND_ (백광인)'},
            'thumbnail': {'url': image_url},
            'author': {
                'name': '코딩 교육 도우미 봇',
                'icon_url': image_url
            },
            'color': 2067276,
            'type': 'rich',
            'description': '',
            'title': ''
        }

    def command(self):
        self.embed['title'] = ":loudspeaker:  **명령어** 안내"
        self.embed['description'] = '''
            **코딩 교육 봇** 은 여러분께 다양한 명령어들을 지원합니다.

            - **!lesson select** : 자신이 듣는 과목을 선택하기.
            - **!lesson question** : 선생님을 불러 질문을 하기.
            - **!lesson author** : 선생님의 자기 소개를 봅니다.
            - **!lesson info <lang>** : 과목 별 안내사항을 봅니다.

            - **!timetable show <mon~fri>** : 요일 별 시간표를 봅니다.
            - **!timetable show <mon~fri>** : 요일 별 시간표를 봅니다.

            그 외에도 봇은 많은 명령어들을 지원하니, 한번 사용해보세요!
            ⠀
            '''
        return nextcord.Embed.from_dict(self.embed)

    def welcome(self):
        self.embed['title'] = ":tada:  서버에 오신 것을 환영합니다!"
        self.embed['description'] = '''
            - 코딩 교육 원격 수업 **디스코드 채널**에 오신 것을 환영합니다!
            - 저는 코딩 교육 강사로 소속된 **[백광인 강사]** 라고 합니다.
            
            - 수업과 관련된 질문이나 문의는 이곳 채널에서 부탁드립니다!
            - 선생님과 함께 열심히 코딩 공부를 즐겁고! 신나게 해봐요!
            ⠀
            '''
        return nextcord.Embed.from_dict(self.embed)

    def introduce(self):
        self.embed['title'] = ":loudspeaker:  코딩 강사 소개"
        self.embed['description'] = '''
            - {0:<6} : **백광인**
            - {1:<6} : **Python, MakeCode**
            - {2:<7} : **010-7167-0851**
            - {3:<7} : **gwangin1999@naver.com**
            '''.format("강사 이름", "교육 언어", "연락처", "이메일")
        return nextcord.Embed.from_dict(self.embed)

    def question(self):
        self.embed['title'] = ":loudspeaker:  선생님께 질문하기"
        self.embed['description'] = '''
            선생님에게 질문하고 싶은 게 있나요? 아주 좋아요!
            선생님이 오시기 전에 물어보고 싶은 내용이 있다면
            미리 정리를 해놓으면 더욱 좋습니다!
            ⠀
            '''
        return nextcord.Embed.from_dict(self.embed)

    def notice(self, day: str, time: int, dateformat: str):
        self.embed['title'] = f":loudspeaker:  {day} {time}시 수업 시작 알림"
        self.embed['description'] = '''
            수업이 시작되기 전에 미리 안내 메세지를 보냈어요.
            이 안내 메세지는 수업 시작 **5분 전에** 발송됩니다!
            
            수업에 늦지 않도록 **사전 준비**를 마저 마쳐주세요.
            **마이크, 스피커**가 잘 작동하는지도 확인 해주세요!
            ⠀
            '''
        self.embed['footer']['text'] = "안내 발송 일자 : " + dateformat
        embed = nextcord.Embed.from_dict(self.embed)
        embed.add_field(name=':one:  Python⠀⠀', value="Python IDLE 프로그램 실행⠀⠀⠀⠀\n지난주 학습했던 내용 복습\n")
        embed.add_field(name=':two:  MakeCode⠀⠀', value="Code Connection for Minecraft\nMinecraft Window Edition 실행\n")

        return embed

    def select_lang_default(self):
        self.embed['title'] = ":speech_left:  수강 과목 선택"
        self.embed['description'] = '''
            디스코드 서버에서 특별한 역할을 받고 싶나요?
            그렇다면 아래 버튼을 눌러서 역할을 받으세요!
            
            단, 자신이 듣는 과목의 버튼을 눌러야 해요!
            그렇지 않으면 선생님이 역할을 바꿀거에요!
            ⠀
            '''
        self.embed['footer']['text'] = "10초 후 메세지가 사라집니다..."
        return nextcord.Embed.from_dict(self.embed)

    def select_lang_failed(self):
        self.embed['title'] = ":speech_left:  수강 과목 선택"
        self.embed['description'] = '''
            이런, 제때 버튼을 누르지 않은 것 같네요..
            하지만 메세지가 사라져도 걱정 하지 마세요!

            !lesson select 명령어를 다시 입력하면
            다시 버튼을 선택하라는 글이 나올 거에요!
            ⠀
            '''
        embed = nextcord.Embed.from_dict(self.embed)
        embed.add_field(name=':x: 시간 만료', value='\n시간이 만료되어 과목 선택이 취소되었습니다.')
        return embed

    def select_lang_success(self, lang):
        self.embed['title'] = ":speech_left:  과목 선택 완료"
        self.embed['description'] = '''
            혹시 제대로 역할을 받았나요? 아주 훌륭해요!
            이제 닉네임이 예쁜 초록색으로 보일 거에요!
            ⠀
            '''
        embed = nextcord.Embed.from_dict(self.embed)
        if lang is None:
            embed.add_field(name=':one: Python', value='\nPython 학습 대상')
            embed.add_field(name=':two: Makecode', value='\nMakecode 학습 대상')
        else:
            embed.add_field(name=':white_check_mark: 선택 완료', value=f'\n성공적으로 {lang} 과목을 선택했습니다!')
        return embed

    def timetable_daily(self, course_list: list):
        self.embed['title'] = ":alarm_clock:  수업 시간표 열람"
        self.embed['description'] = """
            선생님이 진행 중인 수업 시간표를 보여줄게요.
            잘 보고 나서 당일 수업에 늦지 않도록 해요!
            ⠀
            """

        time_value = student_value = lang_value = ""
        for course in course_list:
            time_value += f"⠀⠀  **{course['time']}**시 수업\n"
            student_value += f"⠀⠀  **{course['name']}**\n"
            lang_value += f"⠀⠀  **{course['course']}**\n"

        embed = nextcord.Embed.from_dict(self.embed)
        embed.add_field(name=':one:  수업 시간⠀⠀⠀⠀', value=time_value)
        embed.add_field(name=':two:  디스코드⠀⠀⠀⠀', value=student_value)
        embed.add_field(name=':three:  수강 과목⠀⠀⠀⠀', value=lang_value)

        return embed

    def timetable_daily_failed(self):
        self.embed['title'] = ":alarm_clock:  수업 시간표 열람"
        self.embed['description'] = """
            이런, 혹시 뒤에 요일을 제대로 입력했나요?
            아쉽게도 요일은 영어로만 입력해줘야 해요!
            
            사용 가능한 요일 : **[Mon, Tue, Wed, Thu, Fri]**
            시간표가 궁금하면 다시 명령어를 입력해봐요!
            ⠀⠀
            """
        embed = nextcord.Embed.from_dict(self.embed)
        embed.add_field(name=':x: 열람 실패', value='\n올바른 요일을 작성하지 않았습니다.')
        return embed

    def timetable_daily_empty(self):
        self.embed['title'] = ":alarm_clock:  수업 시간표 열람"
        self.embed['description'] = """
            음, 해당 요일에는 수업이 존재하지 않아요.
            다른 요일에는 수업이 있을지도 모르겠네요!
            ⠀⠀
            """
        embed = nextcord.Embed.from_dict(self.embed)
        embed.add_field(name=':x: 열람 실패', value='\n해당 요일에는 수업 일정이 비어 있습니다.')
        return embed

    def timetable_modify(self, course_list: list, status: str):
        modify = {"add": "추가", "del": "삭제"}
        self.embed['title'] = ":alarm_clock:  수업 시간표 수정"
        self.embed['description'] = f"""
            성공적으로 해당 시간대의 수업표를 {modify[status]}했어요!
            아래에 수정하신 시간표의 정보를 보여드릴게요!
            
            :white_check_mark: **{modify[status]} 완료**
            성공적으로 해당 학생의 시간표를 {modify[status]}했습니다!
            ⠀
            """
        # 해당 요일의 시간표가 존재한다면, 관련 정보를 출력시킴.
        if course_list:
            time_value = student_value = lang_value = ""
            for course in course_list:
                time_value += f"⠀⠀  **{course['time']}**시 수업\n"
                student_value += f"⠀⠀  **{course['name']}**\n"
                lang_value += f"⠀⠀  **{course['course']}**\n"

                embed = nextcord.Embed.from_dict(self.embed)
                embed.add_field(name=':one:  수업 시간⠀⠀⠀⠀', value=time_value)
                embed.add_field(name=':two:  디스코드⠀⠀⠀⠀', value=student_value)
                embed.add_field(name=':three:  수강 과목⠀⠀⠀⠀', value=lang_value)
                return embed
        else:
            embed = nextcord.Embed.from_dict(self.embed)
            embed.add_field(name=':x: 수업 없음', value="\n해당 요일에는 더 이상 수업이 존재하지 않습니다.")
            return embed

    def timetable_add_failed(self, reason: str):
        self.embed['title'] = ":alarm_clock:  시간표 추가 실패"
        self.embed['description'] = """
            이런... 명령어를 입력하는 과정에서 약간의
            문제가 생긴 것 같아요. 다시 한번 양식들을
            잘 읽어보시고 명령어를 재입력해주세요!

            양식 : **[!timeadd <요일> <시간> <학생>]**

            제대로 입력이 되었다면 수업이 추가될 거에요!
            ⠀⠀
            """
        embed = nextcord.Embed.from_dict(self.embed)
        if reason == "day":
            embed.add_field(name=':x: 추가 실패', value="\n올바르지 않은 요일을 입력하였습니다.")
        elif reason == "time":
            embed.add_field(name=':x: 추가 실패', value="\n시간은 18시부터 22시까지 가능합니다.")
        elif reason == "student":
            embed.add_field(name=':x: 추가 실패', value="\n해당 학생은 서버에 존재하지 않습니다.")
        elif reason == "course":
            embed.add_field(name=':x: 추가 실패', value="\n해당 학생은 특정한 과목 역할이 없습니다.")
        elif reason == "wrong":
            embed.add_field(name=':x: 추가 실패', value="\n명령어 양식이 올바르지 않습니다.")
        return embed

    def timetable_modify_failed(self, status: str):
        self.embed['title'] = ":alarm_clock:  수업 시간표 수정"
        if status == "add":
            self.embed['description'] = """
                이미 해당 시간대에는 다른 수업이 존재해요.
                만약 이를 바꾸고 싶다면 먼저 해당 시간대에
                저장된 수업을 제거해주셔야 등록이 가능해요!
    
                삭제 : **[!timemod del <요일> <시간>]**
    
                제대로 삭제가 되었다면 수업이 추기될 거에요!
                ⠀⠀
                """
            embed = nextcord.Embed.from_dict(self.embed)
            embed.add_field(name=':x: 수정 실패', value="\n이미 해당 시간대에 수업이 존재합니다.")
            return embed

        elif status == "del":
            self.embed['description'] = """
                이미 해당 시간대에는 수업이 없는 상태에요...
                수업 삭제는 오직 존재하는 시간에만 가능해요!

                추가 : **[!timemod add <요일> <시간> <이름> <과목>]**

                우선, 빈 시간표를 먼저 채워보는 건 어떨까요?
                ⠀⠀
                """
            embed = nextcord.Embed.from_dict(self.embed)
            embed.add_field(name=':x: 삭제 실패', value="\n해당 시간대에 수업이 존재하지 않습니다.")
            return embed


class SelectClassView(View):

    def __init__(self):
        super().__init__()
        self.timeout = 10.0
        self.lang = None
        self.role = {"Python": os.environ.get('PYTHON_ROLE_ID'), "MakeCode": os.environ.get('MAKECODE_ROLE_ID')}
        self.embed = EmbedMessage()

    @nextcord.ui.button(label='⠀⠀⠀⠀⠀⠀Python⠀⠀⠀⠀⠀⠀⠀', style=nextcord.ButtonStyle.primary)
    async def select_python(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        self.lang = "Python"
        self.stop()
        await interaction.response.send_message(
            f"{interaction.user.mention} 님, 성공적으로 **Python** 과목 역할을 받으셨습니다!",
            embed=self.embed.select_lang_success(self.lang), ephemeral=True
        )

    @nextcord.ui.button(label='⠀⠀⠀⠀⠀MakeCode⠀⠀⠀⠀⠀', style=nextcord.ButtonStyle.secondary)
    async def select_makecode(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        self.lang = "MakeCode"
        self.stop()
        await interaction.response.send_message(
            f"{interaction.user.mention} 님, 성공적으로 **MakeCode** 과목 역할을 받으셨습니다!",
            embed=self.embed.select_lang_success(self.lang), ephemeral=True
        )
