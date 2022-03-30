from typing import Any

import pymysql
import pymysql.cursors
import nextcord
import os

'''
    Timetable 클래스는 mysql.json 의 이차원 딕셔너리 파일을 탐색합니다.
    self.json[day][time] : 해당 요일과 시간대를 수강하는 학생의 정보를 딕셔너리로 받습니다.
    리턴 형식은 {"Student":값, "Class":값} 입니다.
'''


class Timetable:
    def __init__(self):
        self.timetable = pymysql.connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PW'),
            db=os.environ.get('MYSQL_DB'),
            charset='utf8'
        )
        # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
        self.cursor = self.timetable.cursor(pymysql.cursors.DictCursor)

    # 해당 학생이 현재 수강 중인 수업 정보를 리턴하는 함수
    def find_student(self, student: nextcord.Member) -> dict[str, Any] | None:

        # 입력 받은 학생의 수업 데이터 중, 이름과 과목 명만 SELECT 하여 불러옴
        sql = "SELECT * FROM course where name = %s"
        self.cursor.execute(sql, (student))
        data = self.cursor.fetchall()

        """ cursor의 sql 구문을 통해 나온 데이터는 list 형태로 리턴
            list 의 요소는 Dict {'discordID': 'id', 'name': '이름', 'course': '과목', 'weekday', '요일', 'time': datetime}
            list 내부의 data 가 있다면 해당 data Dict 를 리턴 """
        if data:
            return data[0]

    # 해당 요일과 시간에 해당되는 수업 정보를 리턴하는 함수
    def find_course(self, day: str, time: int) -> dict[str, Any] | None:

        # 먼저, 입력 받은 시간대에 다른 수업이 있는지를 SELECT로 탐색함
        sql = "SELECT * FROM course where weekday = %s AND time = %s"
        self.cursor.execute(sql, (day, time))
        data = self.cursor.fetchall()

        if data:
            return data[0]

    # 특정 수업 시간에 학생의 수강 정보를 집어 넣는 함수
    # True 리턴 시 정상적인 수강 정보 추가, False 리턴 시 시간표 겹침으로 인한 추가 실패 안내
    def add_student(self, day: str, time: str, course: str, student: nextcord.Member) -> None:

        # 새롭게 입력받은 정보를 정리하여 INSERT 로 추가함.
        try:
            sql = """INSERT INTO course(discordID, name, course, time, weekday) 
                            values (%s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, (student.id, student, course, time, day))

        # 이미 기존에 시간표가 설정된 경우, 다른 시간대로 강의 정보를 수정함
        except pymysql.err.IntegrityError:
            sql = "UPDATE course SET time = %s, weekday = %s WHERE name = %s"
            self.cursor.execute(sql, (time, day, student))

        finally:
            self.timetable.commit()

    # 특정 수업 시간에 학생의 수강 정보를 삭제하는 함수
    def remove_student(self, student: nextcord.Member) -> None:

        # 입력 받은 학생의 데이터를 MySQL 에서 완전히 삭제시킴
        sql = "DELETE FROM course where name = %s"
        self.cursor.execute(sql, (student.nick))
        self.timetable.commit()

    # 특정 요일의 시간표 정보를 List[Tuple(시간, 학생, 과목)] 으로 return 해주는 함수
    def get_day_class(self, day: str) -> list[dict[str, Any], ...] | None:

        # 입력 받은 학생의 수업 데이터 중, 이름과 과목 명만 SELECT 하여 불러옴
        sql = "SELECT time, name, course FROM course where weekday = %s"
        self.cursor.execute(sql, (day))
        data = self.cursor.fetchall()

        if data:
            return data

    # 디스코드 봇 종료 시 MySQL 서버와의 통신을 종료하는 함수 (event / on_disconnect())
    def close_mysql(self):
        self.timetable.commit()
        self.timetable.close()
