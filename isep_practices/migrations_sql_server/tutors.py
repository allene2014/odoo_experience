# -*- coding: utf-8 -*-

from sqlalchemy import and_
from sql_conn import PracticasTutores, get_session_server_isep, get_pg_session, \
    ResPartner

# SQL SERVER SESSION
session_server = get_session_server_isep()
practicas_tutores = session_server.query(PracticasTutores).filter(
    and_(PracticasTutores.DNI is not None,
         PracticasTutores.DNI != '')).all()
# POSTGRES SERVER SESSION
session_pg = get_pg_session()

for practicas_tutor in practicas_tutores:
    try:
        tutor = session_pg.query(ResPartner).filter(
            and_(ResPartner.tutor == True, ResPartner.dni ==
                 practicas_tutor.DNI)).first()

        if tutor is None:
            tutor = ResPartner()
            tutor.tutor = True
            tutor.active = True
            tutor.company_id = 1
            tutor.name = ' '.join([practicas_tutor.Nombres,
                                   practicas_tutor.Apellidos])
            tutor.display_name = ' '.join([practicas_tutor.Nombres,
                                           practicas_tutor.Apellidos])
            tutor.email = practicas_tutor.EMail
            tutor.dni = practicas_tutor.DNI
            session_pg.add(tutor)
            session_pg.commit()
            print("Tutor created:", tutor.id)
        else:
            print("Tutor already exist:", tutor.id)
    except Exception as e:
        print(e)
