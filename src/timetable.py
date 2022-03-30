from typing import Any

import pymysql
import pymysql.cursors
import nextcord
import os


def connect_mysql() -> tuple:
    # 수업 정보를 가져올 때마다 MySQL에 연결을 실행해야 함.
    timetable = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PW'),
        db=os.getenv('MYSQL_DB'),
        charset='utf8'
    )
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    cursor = timetable.cursor(pymysql.cursors.DictCursor)
    return timetable, cursor


# 해당 학생이 현재 수강 중인 수업 정보를 리턴하는 함수
def find_student(student: nextcord.Member) -> dict[str, Any] | None:

    timetable, cursor = connect_mysql()

    # 입력 받은 학생의 수업 데이터 중, 이름과 과목 명만 SELECT 하여 불러옴
    sql = "SELECT * FROM course where name = %s"
    cursor.execute(sql, (student))
    data = cursor.fetchall()
    timetable.close()

    """ cursor의 sql 구문을 통해 나온 데이터는 list 형태로 리턴
        list 의 요소는 Dict {'discordID': 'id', 'name': '이름', 'course': '과목', 'weekday', '요일', 'time': '시간'}
        list 내부의 data 가 있다면 해당 data Dict 를 리턴 """
    if data:
        return data[0]


# 해당 요일과 시간에 해당되는 수업 정보를 리턴하는 함수
def find_course(day: str, time: int) -> dict[str, Any] | None:

    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    timetable, cursor = connect_mysql()

    # 먼저, 입력 받은 시간대에 다른 수업이 있는지를 SELECT로 탐색함
    sql = "SELECT * FROM course where weekday = %s AND time = %s"
    cursor.execute(sql, (day, time))
    data = cursor.fetchall()
    timetable.close()

    if data:
        return data[0]


# 특정 수업 시간에 학생의 수강 정보를 집어 넣는 함수
# True 리턴 시 정상적인 수강 정보 추가, False 리턴 시 시간표 겹침으로 인한 추가 실패 안내
def add_student(day: str, time: int, course: str, student: nextcord.Member) -> None:

    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    timetable, cursor = connect_mysql()

    # 새롭게 입력받은 정보를 정리하여 INSERT 로 추가함.
    try:
        sql = """INSERT INTO course(discordID, name, course, time, weekday) 
                        values (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (student.id, student, course, time, day))

    # 이미 기존에 시간표가 설정된 경우, 다른 시간대로 강의 정보를 수정함
    except pymysql.err.IntegrityError:
        sql = "UPDATE course SET time = %s, weekday = %s WHERE discordID = %s"
        cursor.execute(sql, (time, day, student.id))

    finally:
        timetable.commit()
        timetable.close()


# 특정 수업 시간에 학생의 수강 정보를 삭제하는 함수
def remove_student(student: nextcord.Member) -> None:

    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    timetable, cursor = connect_mysql()

    # 입력 받은 학생의 데이터를 MySQL 에서 완전히 삭제시킴
    sql = "DELETE FROM course where name = %s"
    cursor.execute(sql, (student))
    timetable.commit()
    timetable.close()


# 특정 요일의 시간표 정보를 List[dict{ data... }] 으로 return 해주는 함수
def get_day_class(day: str) -> tuple[dict[str, Any], ...]:

    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    timetable, cursor = connect_mysql()

    # 입력 받은 학생의 수업 데이터 중, 이름과 과목 명만 SELECT 하여 불러옴 (시간 순서대로 정렬)
    sql = "SELECT time, name, course FROM course where weekday = %s ORDER BY time DESC"
    cursor.execute(sql, (day))
    data = cursor.fetchall()
    timetable.close()

    if data:
        return data
