# -*- coding: utf-8 -*-

from sqlalchemy import and_
from sql_conn import PracticasCentros, get_session_server_isep, get_pg_session, \
    Center

# SQL SERVER SESSION
session_server = get_session_server_isep()
practicas_centro = session_server.query(PracticasCentros).filter(
    and_(PracticasCentros.NombreOficial is not None,
         PracticasCentros.NombreOficial != '')).all()

# POSTGRES SERVER SESSION
session_pg = get_pg_session()

for practice_center in practicas_centro:
    try:
        center = session_pg.query(Center).filter(
            and_(Center.center == True, Center.name_official ==
                 practice_center.NombreOficial)).first()

        if center is None:
            center = Center()
            center.center = True
            center.active = True
            center.company_id = 1
            center.practice_schedule_id = None
            center.name = practice_center.Nombre
            center.display_name = practice_center.Nombre
            center.vat = practice_center.NIF
            center.name_official = practice_center.NombreOficial
            center.coordinator = practice_center.Coordinador
            center.maximum_places = practice_center.MaximoPlazas
            center.phone = practice_center.Telefono
            center.website = practice_center.Web
            center.street = practice_center.Direccion
            center.x_sexo = practice_center.SexoFirmante
            center.email = practice_center.EMail
            center.signatory = practice_center.Firmante
            center.city = practice_center.Poblacion
            center.observation = practice_center.Observaciones
            if len(practice_center.CodPostal) == 4:
                center.zip = '0' + practice_center.CodPostal
            else:
                center.zip = practice_center.CodPostal
            session_pg.add(center)
            session_pg.commit()
            print("Center created: ", center.id)
        else:
            print("Center Already exist: ", center.id)
    except Exception as e:
        print(e)
