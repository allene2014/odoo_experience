# -*- coding: utf-8 -*-

from sql_conn import get_pg_session, ResPartner, PracticeCenterTutor
from sqlalchemy import and_
from op_sql import SQL

session_pg = get_pg_session()

sql_server = SQL()
centro_tutor_rels = sql_server.get_all_center_tutors_rel()

for centro_tutor in centro_tutor_rels:
    try:
        center = session_pg.query(ResPartner).filter(
            and_(ResPartner.center == True, ResPartner.name_official ==
                 centro_tutor.get('NombreOficial'))).first()
        tutor = session_pg.query(ResPartner).filter(
            and_(ResPartner.tutor == True,
                 ResPartner.dni == centro_tutor.get('DNI'))).first()

        if center is None:
            print("Center not found: ", centro_tutor.get('NombreOficial'))
            continue
        if tutor is None:
            print(centro_tutor.get('DNI'))
            continue

        center_tutor = session_pg.query(PracticeCenterTutor).filter(
            and_(PracticeCenterTutor.partner_id == center.id,
                 PracticeCenterTutor.tutor_id == tutor.id)).first()

        if center_tutor is None:
            center_tutor = PracticeCenterTutor()
            center_tutor.tutor = True
            center_tutor.active = True
            center_tutor.partner_id = center.id
            center_tutor.tutor_id = tutor.id
            session_pg.add(center_tutor)
            session_pg.commit()
            print("Center tutor created:", [center.id, tutor.id])
        else:
            print("Center tutor already exist:", [center.id, tutor.id])
    except Exception as e:
        print(e)
