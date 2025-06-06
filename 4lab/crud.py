from sqlalchemy.orm import Session
import models, schemas

def get_teachers(db: Session):
    return db.query(models.Teacher).all()

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def delete_teacher(db: Session, teacher_id: int):
    teacher = get_teacher(db, teacher_id)
    if teacher:
        db.delete(teacher)
        db.commit()

def get_courses(db: Session):
    return db.query(models.Course).all()

def get_courses_by_teacher(db: Session, teacher_id: int):
    return db.query(models.Course).filter(models.Course.teacher_id == teacher_id).all()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
