from enum import Enum

class States(Enum):
    S_START = "0"
    S_START_STUD = "1"
    S_START_TEACH = "2"
    S_NORMAL = "3"
    S_TIMETABLE = "4"
    S_LOCATION = "5"
    S_CLEAR = "7"