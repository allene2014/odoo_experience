# -*- coding: utf-8 -*-

from sql_conn import get_pg_session, PracticasTemarios, PracticeTemary, \
    get_session_server_isep, OpCourse

session_server = get_session_server_isep()
temarios = session_server.query(PracticasTemarios).all()

session_pg = get_pg_session()

for temario in temarios:
    try:
        course = session_pg.query(OpCourse).filter(
            OpCourse.code == temario.Curso_Id[-2:]).first()
        temary = session_pg.query(PracticeTemary).filter(
            PracticeTemary.name == temario.Nombre).first()

        if course is None:
            print("Course not found: ", temario.Curso_Id)
            continue

        if temary is None:
            temary = PracticeTemary()
            temary.active = True
            temary.content = temario.Contenido
            temary.op_course_id = course.id
            temary.name = temario.Nombre
            session_pg.add(temary)
            session_pg.commit()
            print("Temary created:", temary.id)
        else:
            print("Temary already exist:", temary.id)

    except Exception as e:
        print(e)
        continue

