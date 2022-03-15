import nextcord
from nextcord.ui import View


class EmbedMessage(nextcord.Embed):
    def __init__(self):
        super().__init__()
        self.embed = nextcord.Embed(title="코딩 교육 알리미 봇", colour=nextcord.Colour.dark_green())
        self.embed.set_footer(text="Created by RookieAND_")
        self.embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/2568/PNG/512/code_coding_icon_153713.png")

    def command(self):
        desc = '''
        - !lesson install : 수업 관련 프로그램 설치 안내문을 봅니다
        - !lesson time : 금일 진행될 수업의 일정표를 미리 열람합니다
        - !lesson author : 교육 봇의 제작자에 대한 정보를 열람합니다
        '''
        self.embed.clear_fields()
        self.embed.add_field(name=":desktop: lesson 명령어 안내", value=desc)
        return self.embed

    def welcome(self):
        desc = '''
        - 코딩 교육 원격 수업 디스코드 채널에 오신 것을 환영합니다!
        - 저는 코딩 교육 강사로 소속된 **[백광인 강사]** 라고 합니다.
        - 수업과 관련된 질문이나 문의는 이곳 채널에서 부탁드립니다!
        '''
        self.embed.clear_fields()
        self.embed.add_field(name=":clap: 코딩 교육에 오신 것을 환영해요!", value=desc)
        return self.embed

    def introduce(self):
        desc = '''
        - 강사 이름 : **백광인**
        - 교육 언어 : **Python, MakeCode**
        - 연락처 : **010-7167-0851**
        - 이메일 : **gwangin1999@naver.com**
        '''
        self.embed.clear_fields()
        self.embed.add_field(name=":student: 코딩 교육 강사 소개", value=desc)
        return self.embed

    def question(self):
        desc = '''
        - 강사 이름 : **백광인**
        - 교육 언어 : **Python, MakeCode**
        - 연락처 : **010-7167-0851**
        - 이메일 : **gwangin1999@naver.com**
        '''
        self.embed.clear_fields()
        self.embed.add_field(name=":student: 코딩 교육 강사 소개", value=desc)
        return self.embed

    def select_lang(self, lang):
        self.embed.clear_fields()
        if lang is None:
            self.embed.add_field(name=":student: Python", value="현재 파이썬을 배우는 학생")
            self.embed.add_field(name=":student: Makecode", value="현재 Makecode를 배우는 학생")
        else:
            self.embed.add_field(name=":student: 수강 과목 선택 완료!", value=f"성공적으로 {lang} 과목을 선택했습니다!")
        return self.embed


class SelectClassView(View):

    def __init__(self):
        super().__init__()
        self.lang = None
        self.role = {"Python": 947519272278708224, "MakeCode": 947517959474139146}
        self.embed = EmbedMessage()

    @nextcord.ui.button(label='Python', style=nextcord.ButtonStyle.primary, row=0)
    async def select_python(self, interaction: nextcord.Interaction):
        self.lang = "Python"
        self.stop()
        await interaction.response.send_message(
            embed=self.embed.select_lang(self.lang),
            ephemeral=True, delete_after=3.0
        )

    @nextcord.ui.button(label='MakeCode', style=nextcord.ButtonStyle.secondary, row=0)
    async def select_makecode(self, interaction: nextcord.Interaction):
        self.lang = "MakeCode"
        self.stop()
        await interaction.response.send_message(
            embed=self.embed.select_lang(self.lang),
            ephemeral=True, delete_after=3.0
        )
