from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, models
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.CourseRead])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)

@router.post("/", response_model=schemas.CourseRead, status_code=201)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    teacher = crud.get_teacher(db, course.teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return crud.create_course(db, course)

@router.delete("/{id}", status_code=204)
def delete_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    crud.delete_course(db, id)
