from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select


# ===================== МОДЕЛИ =====================

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    group: str = Field(index=True)
    secret_note: str


class StudentUpdate(SQLModel):
    # Все поля опциональны для PATCH
    name: str | None = None
    age: int | None = None
    group: str | None = None
    secret_note: str | None = None


class Skill(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # связь с Student
    student_id: int | None = Field(default=None, foreign_key="student.id")
    name: str
    level: int = 1  # уровень навыка


class Achievement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # связь с Student
    student_id: int | None = Field(default=None, foreign_key="student.id")
    title: str
    description: str | None = None


# ===================== НАСТРОЙКА БД =====================

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# ===================== ПРИЛОЖЕНИЕ =====================

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ===================== STUDENT =====================

@app.post("/students/")
def create_student(student: Student, session: SessionDep) -> Student:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@app.get("/students/")
def read_students(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Student]:
    students = session.exec(
        select(Student).offset(offset).limit(limit)
    ).all()
    return students


@app.get("/students/{student_id}")
def read_student(student_id: int, session: SessionDep) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}")
def update_student(
    student_id: int,
    data: StudentUpdate,
    session: SessionDep,
) -> Student:
    student_db = session.get(Student, student_id)
    if not student_db:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student_db, key, value)

    session.add(student_db)
    session.commit()
    session.refresh(student_db)
    return student_db


@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: SessionDep):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"ok": True}


# ===================== SKILLS (СКИЛЛЫ) =====================

@app.post("/students/{student_id}/skills/")
def add_skill(student_id: int, skill: Skill, session: SessionDep) -> Skill:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Привязываем скилл к студенту
    skill.student_id = student_id
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@app.get("/students/{student_id}/skills/")
def get_student_skills(
    student_id: int,
    session: SessionDep,
) -> list[Skill]:
    skills = session.exec(
        select(Skill).where(Skill.student_id == student_id)
    ).all()
    return skills


# ===================== ACHIEVEMENTS (ЗАСЛУГИ) =====================

@app.post("/students/{student_id}/achievements/")
def add_achievement(
    student_id: int,
    achievement: Achievement,
    session: SessionDep,
) -> Achievement:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    achievement.student_id = student_id
    session.add(achievement)
    session.commit()
    session.refresh(achievement)
    return achievement


@app.get("/students/{student_id}/achievements/")
def get_student_achievements(
    student_id: int,
    session: SessionDep,
) -> list[Achievement]:
    achievements = session.exec(
        select(Achievement).where(Achievement.student_id == student_id)
    ).all()
    return achievements
