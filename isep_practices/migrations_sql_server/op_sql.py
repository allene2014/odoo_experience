# -*- coding: utf-8 -*-
from dotenv import load_dotenv, find_dotenv
import logging
import pyodbc
import os

logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())


class SQL():
    dsn = 'egServer70source'
    server = os.environ['SERVER']
    user = os.environ['MSSQL_USER']
    password = os.environ['MSSQL_PASSWORD']
    database = os.environ['MSSQL_DATABASE']
    port = os.environ['MSSQL_PORT']
    driver = 'SQL Server'  # for Windows
    if os.name == "posix":
        driver = 'ODBC Driver 17 for SQL Server'  # for linux

    def query(self, sql):
        logger.info(sql)
        con_string = 'DRIVER={' \
                     '%s};SERVER=%s;UID=%s;PWD=%s;DATABASE=%s;PORT=%s' % (
                         self.driver, self.server, self.user, self.password,
                         self.database, self.port)
        conn = pyodbc.connect(con_string)
        cursor_sql = conn.cursor()
        cursor_sql.execute(sql)
        columns = [column[0] for column in cursor_sql.description]
        return [dict(zip(columns, row)) for row in cursor_sql.fetchall()]

    def query_get_one(self, sql):
        con_string = 'DRIVER={' \
                     '%s};SERVER=%s;UID=%s;PWD=%s;DATABASE=%s;PORT=%s' % (
                         self.driver, self.server, self.user, self.password,
                         self.database, self.port)
        conn = pyodbc.connect(con_string)
        cursor_sql = conn.cursor()
        cursor_sql.execute(sql)
        return cursor_sql.fetchone()

    def get_all_center_tutors_rel(self):
        return self.query(
            "SELECT pct.*, pc.NombreOficial, pt.DNI "
            "FROM PracticasCentrosTutor pct "
            "INNER JOIN PracticasCentros pc ON pct.CentroId = pc.ID "
            "INNER JOIN PracticasTutores pt ON pct.TutorId = pt.ID "
            "WHERE pt.DNI != '' and pt.DNI IS NOT NULL;"
        )
