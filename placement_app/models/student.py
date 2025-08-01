from dataclasses import dataclass

@dataclass
class Student:
    student_id: int
    name: str
    age: int
    gender: str
    email: str
    phone: str
    enrollment_year: int
    course_batch: str
    city: str
    graduation_year: int
