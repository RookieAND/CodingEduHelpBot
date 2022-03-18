import json

'''
    Timetable 클래스는 timetable.json 의 이차원 딕셔너리 파일을 탐색합니다.
    self.json[day][time] : 해당 요일과 시간대를 수강하는 학생의 정보를 딕셔너리로 받습니다.
    리턴 형식은 {"Student":값, "Class":값} 입니다.
'''


class Timetable:
    def __init__(self):
        with open('../data/timetable.json', encoding='utf8') as tf:
            self.json = json.load(tf)

    # 해당 수업 시간에 해당되는 학생의 정보 Dict[이름, 과목] 를 리턴하는 함수
    def find_student(self, day: str, time: int) -> dict:
        return self.json[day][time]

    # 특정 수업 시간에 학생의 수강 정보를 집어 넣는 함수
    def add_student(self, day: str, time: str, student: str, lang: str) -> None:
        class_info = self.json[day][time]
        if class_info["Student"] is None or class_info["Class"] is None:
            self.json[day][time].update({"Student": student, "Class": lang})
            self.reload()

    # 특정 수업 시간에 학생의 수강 정보를 삭제하는 함수
    def remove_student(self, day: str, time: str) -> None:
        class_info = self.json[day][time]
        class_info.update({"Student": None, "Class": None})
        self.reload()

    # 특정 요일의 시간표 정보를 List[Tuple(시간, 학생, 과목)] 으로 return 해주는 함수
    def get_day_class(self, day: str) -> list:
        class_list = self.json[day]
        # info 변수는 {학생 이름 : 수강 언어} 값을 담은 Dict 타입
        class_info = list((time, info["Student"], info["Class"]) for time, info in class_list.items())
        return class_info

    # 수정된 timetable 정보가 있다면, 이를 확인해 새롭게 timetable.json 을 작성함
    def reload(self):
        with open('../data/timetable.json', 'w', encoding='utf8') as f:
            json.dump(self.json, f, indent=4, ensure_ascii=False)
