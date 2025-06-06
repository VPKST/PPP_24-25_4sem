from pydantic import BaseModel, ConfigDict, Field

class TeacherBase(BaseModel):
    name: str = Field(..., min_length=1)

class TeacherCreate(TeacherBase): pass

class TeacherRead(TeacherBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CourseBase(BaseModel):
    name: str
    student_count: int
    teacher_id: int

class CourseCreate(CourseBase): pass

class CourseRead(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
