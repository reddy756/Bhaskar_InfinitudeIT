from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    description: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
