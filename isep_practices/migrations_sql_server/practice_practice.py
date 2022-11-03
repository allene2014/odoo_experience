# -*- coding: utf-8 -*-

from sqlalchemy import and_
from sql_conn import PracticePractice, PracticasPracticas, get_pg_session, \
    get_session_server_isep, OpBatch, PracticasTemarios, PracticeTemary, \
    OpStudent, PracticasTutores, ResPartner, PracticasCentros, OpAdmission

session_server = get_session_server_isep()
practicas = session_server.query(
    PracticasPracticas, PracticasTemarios, PracticasTutores,
    PracticasCentros).join(PracticasTemarios, PracticasPracticas.TemarioID ==
                           PracticasTemarios.ID).join(
    PracticasTutores, PracticasPracticas.TutorID ==
                      PracticasTutores.ID).join(
    PracticasCentros, PracticasPracticas.CentroID ==
                      PracticasCentros.ID).filter(
    and_(PracticasTutores.DNI is not None, PracticasTutores.DNI != '')).all()

session_pg = get_pg_session()

for practica in practicas:
    try:
        batch = session_pg.query(OpBatch).filter(
            OpBatch.code == practica.PracticasPracticas.Curso_Id.strip()).first()
        temary = session_pg.query(PracticeTemary).filter(
            PracticeTemary.name == practica.PracticasTemarios.Nombre).first()
        student = session_pg.query(OpStudent).filter(
            OpStudent.n_id == str(practica.PracticasPracticas.N_Id)).first()
        tutor = session_pg.query(ResPartner).filter(and_(
            ResPartner.tutor == True, ResPartner.dni ==
            practica.PracticasTutores.DNI)).first()
        center = session_pg.query(ResPartner).filter(and_(
            ResPartner.center == True, ResPartner.name_official ==
            practica.PracticasCentros.NombreOficial)).first()

        if batch is None:
            print("Batch not found: ", practica.PracticasPracticas.Curso_Id)
            continue
        if temary is None:
            print("[INFO]: Temary not found: ", practica.PracticasTemarios.Nombre)
        if student is None:
            print("Student not found: ", practica.PracticasPracticas.N_Id)
            continue
        if tutor is None:
            print("Tutor not found: ", practica.PracticasTutores.DNI)
            continue
        if center is None:
            print("Center not found: ",
                  practica.PracticasCentros.NombreOficial)
            continue

        practice = session_pg.query(PracticePractice).filter(
            and_(PracticePractice.op_student_id == student.id,
                 PracticePractice.op_course_id == batch.course_id,
                 PracticePractice.center_id == center.id)).first()

        admission = session_pg.query(OpAdmission).filter(and_(
            OpAdmission.student_id == student.id, OpAdmission.batch_id ==
            batch.id)).first()
        admission_id = None
        if admission is not None:
            admission_id = admission.id
        else:
            print("[INFO]: Admission not found")

        if practice is None:
            status_phase = None
            if practica.PracticasPracticas.FaseID in [1, 2]:
                status_phase = 'in progress'
            elif practica.PracticasPracticas.FaseID == 3:
                status_phase = 'started'
            elif practica.PracticasPracticas.FaseID == 4:
                status_phase = 'finished'

            payment_center = False
            if practica.PracticasPracticas.RetribucionCentro > 0:
                payment_center = True

            practice = PracticePractice()
            practice.active = True
            practice.op_student_id = student.id
            practice.op_course_id = batch.course_id
            practice.op_admission_id = admission_id
            practice.weekly_hours = practica.PracticasPracticas.HorasSemanales
            practice.total_hours = practica.PracticasPracticas.HorasTotales
            practice.start_date = practica.PracticasPracticas.FechaInicio
            practice.final_date = practica.PracticasPracticas.FechaFin
            practice.practice_temary_id = temary.id or None
            practice.tutor_id = tutor.id
            practice.center_id = center.id
            practice.status_phase = status_phase
            practice.payment_center = payment_center
            practice.remuneration_center = practica.PracticasPracticas.RetribucionCentro
            session_pg.add(practice)
            session_pg.commit()
            print("Practice created:",
                  [student.id, batch.course_id, center.id])
        else:
            print("Practice already exist:",
                  [student.id, batch.course_id, center.id])
    except Exception as e:
        print(e)
        continue

print("**********  End of script  **********")
