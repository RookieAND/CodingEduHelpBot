import json


class Timetable:
    def __init__(self):
        with open('./data/timetable.json', encoding='utf8') as tf:
            self.json = json.load(tf)

    # 해당 수업 시간에 해당되는 학생의 정보 Dict[이름, 과목] 를 리턴하는 함수
    def find_student(self, day: str, time: int) -> dict:
        info = self.json[day][time]
        return info

    # 특정 수업 시간에 학생의 수강 정보를 집어 넣는 함수
    def add_student(self, day: str, time: int, student: str, lang: str) -> None:
        self.json[day][time] = {"Student": student, "Class": lang}
        self.reload()

    # 특정 수업 시간에 학생의 수강 정보를 삭제하는 함수
    def remove_student(self, day: str, time: int) -> None:
        self.json[day][time] = {"Student": None, "Class": None}
        self.reload()

    # 특정 요일의 시간표를 List[(시간, 학생, 과목)] 으로 리턴하는 함수
    def get_day_class(self, day: str) -> list:
        class_list = self.json[day]
        class_info = []
        for time, info in class_list.items():
            class_info.append((time, info["Student"], info["Class"]))
        return class_info

    # 수정된 timetable이 있다면, 이를 캐치하여 새롭게 json을 작성함
    def reload(self):
        with open('./data/timetable.json', 'r', encoding='utf8') as f:
            json.dump(self.json, f, indent=4)
