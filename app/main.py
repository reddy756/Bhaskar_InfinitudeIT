from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app1 = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)


@app1.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db)):
    db_course = models.Course(name=course.name, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app1.get("/courses/", response_model=list[schemas.Course])
def get_courses(db: Session = Depends(database.get_db)):
    return db.query(models.Course).all()


# New API to get course by ID
@app1.get("/courses/{course_id}", response_model=schemas.Course)
def get_course_by_id(course_id: int, db: Session = Depends(database.get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()

    # Raise an exception if the course is not found
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return db_course
