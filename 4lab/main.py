from fastapi import FastAPI
from routers import teachers, courses
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
