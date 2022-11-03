# -*- coding: utf-8 -*-

from sqlalchemy import and_
from sql_conn import PracticasCentrosCursos, get_session_server_isep, \
    get_pg_session, OpCourse, PracticeCenterCourse, PracticasCentros, Center

session_server = get_session_server_isep()
session_pg = get_pg_session()

centro_curso_rels = session_server.query(
    PracticasCentrosCursos, PracticasCentros).join(
    PracticasCentros, PracticasCentrosCursos.CentroID == PracticasCentros.ID) \
    .all()

for centro_curso in centro_curso_rels:
    try:
        center = session_pg.query(Center).filter(
            and_(Center.center == True,
                 Center.name_official ==
                 centro_curso.PracticasCentros.NombreOficial)).first()
        course = session_pg.query(OpCourse).filter(
            OpCourse.code == centro_curso.PracticasCentrosCursos.Curso_Id[
                             -2:]).first()

        if center is None:
            print("Center not found: ",
                  centro_curso.PracticasCentros.NombreOficial)
            continue
        if course is None:
            print("Course not found: ", centro_curso.Curso_Id)
            continue

        center_course = session_pg.query(PracticeCenterCourse).filter(
            and_(PracticeCenterCourse.partner_id == center.id,
                 PracticeCenterCourse.op_course_id == course.id)).first()

        if center_course is None:
            center_course = PracticeCenterCourse()
            center_course.tutor = True
            center_course.active = True
            center_course.partner_id = center.id
            center_course.op_course_id = course.id
            session_pg.add(center_course)
            session_pg.commit()
            print("Center course created:", [center.id, course.id])
        else:
            print("Center course already exist:", [center.id, course.id])
    except Exception as e:
        print(e)
