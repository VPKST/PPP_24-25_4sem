from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TeacherRead])
def read_teachers(db: Session = Depends(get_db)):
    return crud.get_teachers(db)

@router.post("/", response_model=schemas.TeacherRead, status_code=201)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, teacher)

@router.delete("/{id}", status_code=204)
def delete_teacher(id: int, db: Session = Depends(get_db)):
    teacher = crud.get_teacher(db, id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    crud.delete_teacher(db, id)

@router.get("/{id}/courses", response_model=list[schemas.CourseRead])
def read_courses_by_teacher(id: int, db: Session = Depends(get_db)):
    teacher = crud.get_teacher(db, id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return crud.get_courses_by_teacher(db, id)
