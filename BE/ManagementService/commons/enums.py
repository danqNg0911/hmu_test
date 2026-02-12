from enum import Enum

class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    TEACHER = "teacher"

class StationTypeEnum(str, Enum):
    QUESTIONS = "question_answer"
    INTERVIEW = "patient_interview"

class FindingTypeEnum(str, Enum):
    DESCRIPTION = "description"
    IMAGE = "image"
