import pyodbc
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import smtplib
from email.message import EmailMessage
from datetime import datetime
import random
from urllib.parse import quote, unquote

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=KPC129\\PruebaJT;'
        'DATABASE=Encuestas;'
        'UID=sa;'
        'PWD=PruebaJT12345;'
    )
    return conn

app = Flask(__name__)
app.secret_key = 'response'

@app.route('/')
def generador():
    hoy = datetime.now()
    codigo_fecha = hoy.strftime ("%d%m%y")
    numero_random = str(random.randint(0,9999)).zfill(4)
    codigo_final = f"{codigo_fecha}_{numero_random}"

    session['codigo_final'] = codigo_final
    return render_template('Generador.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    cliente = request.form['cliente']
    email_calidad = request.form['mailCalidad']
    email_entregas = request.form['mailEntregas']    
    email_servicio = request.form['mailServicio']

    cuerpo_calidad = request.form['mensajeCalidad']
    cuerpo_entregas = request.form['mensajeEntregas']
    cuerpo_servicio = request.form['mensajeServicio']

    session['cliente'] = cliente
    codigo_final = session['codigo_final']

    base_url = "http://localhost:5000"

    asunto_calidad = f"Encuesta de Calidad - {cliente}"
    asunto_entregas = f"Encuesta de Entregas - {cliente}"
    asunto_servicio = f"Encuesta de Servicio - {cliente}"

    cliente_codificado = quote(cliente)

    cuerpo_calidad += f"\n\nCompleta la encuesta aquí:\n{base_url}/Calidad?cliente={cliente_codificado}&id={codigo_final}"
    cuerpo_entregas += f"\n\nCompleta la encuesta aquí:\n{base_url}/Entregas?cliente={cliente_codificado}&id={codigo_final}"
    cuerpo_servicio += f"\n\nCompleta la encuesta aquí:\n{base_url}/Servicio?cliente={cliente_codificado}&id={codigo_final}"

    enviar_correo(email_calidad, asunto_calidad, cuerpo_calidad)
    enviar_correo(email_entregas, asunto_entregas, cuerpo_entregas)
    enviar_correo(email_servicio, asunto_servicio, cuerpo_servicio)

    flash('Correos enviados con éxito')
    return redirect(url_for('generador'))


def enviar_correo(destinario, asunto, cuerpo):
    remitente = "noreply@kentek.com.mx"
    password = "Moz06571" 

    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinario
    msg.set_content(cuerpo)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(remitente, password)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error al enviar a {destinario}: {e}")

@app.route('/encuestas', methods=['GET','POST'])
def encuesta():
    return render_template('encuesta.html')

@app.route('/departamento', methods=['POST'])
def departamento():
    departamento = request.form.get('departamento')
    if departamento == 'Calidad':
        return redirect(url_for('backCalidad'))
    elif departamento == 'Entregas':
        return redirect(url_for('backEntregas'))
    else:
        return redirect(url_for('backServicio'))

@app.route('/backCalidad')
def backCalidad():
    return render_template('backCalidad.html')

@app.route('/backEntregas')
def backEntregas():
    return render_template('backEntregas.html')

@app.route('/backServicio')
def backServicio():
    return render_template('backServicio.html')

@app.route('/Calidad')
def Calidad():
    cliente = unquote(request.args.get('cliente'))
    codigo_final = request.args.get('id')
    return render_template('Calidad.html',cliente=cliente, codigo_final=codigo_final)

@app.route('/Entregas')
def Entregas():
    cliente = unquote(request.args.get('cliente'))
    codigo_final = request.args.get('id')
    return render_template('Entregas.html',cliente=cliente, codigo_final=codigo_final)

@app.route('/Servicio')
def Servicio():
    cliente = unquote(request.args.get('cliente'))
    codigo_final = request.args.get('id')
    return render_template('Servicio.html',cliente=cliente, codigo_final=codigo_final)

@app.route('/guardar', methods=['POST'])
def guardar():
    cliente = request.form.get('cliente')
    codigo = request.form.get('codigo')
    departamento = request.form.get('departamento')
    comentarios = request.form.get('comentarios')
    fecha = datetime.now().strftime('%Y-%m-%d')

    preguntas_por_departamento = {
        'Calidad': ['Q1', 'Q2', 'Q3','Q4'],
        'Entregas': ['Q5', 'Q6', 'Q7'],
        'Servicio': ['Q8', 'Q9', 'Q10','Q11', 'Q12', 'Q13'],
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    
    preguntas = preguntas_por_departamento.get(departamento, []) + ['Q14']

    for pregunta in preguntas:
        valor = request.form.get(pregunta)

        cursor.execute( '''
        INSERT INTO Respuestas (ID, Cliente, Departamento, Pregunta, Valor, Fecha)
        VALUES(?,?,?,?,?,?)              
        ''',(
            codigo,
            cliente,
            departamento,
            pregunta,
            valor,
            fecha
        ))
    
    if comentarios:
        cursor.execute('''
            INSERT INTO Comentarios (ID, Departamento, Comentarios, Fecha)
            VALUES (?, ?, ?, ?)
        ''', (
            codigo,
            departamento,
            comentarios,
            fecha
        ))

    conn.commit()
    conn.close()
    session.clear()
    return redirect(url_for('gracias'))


@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route('/resultados', methods = ['POST', 'GET'])
def resultados():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    resumenes_float = []

    conn = get_db_connection()
    cursor = conn.cursor()

    if fecha_inicio and fecha_fin:
        try:
            inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            find_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')

            if inicio_dt > find_dt:
                return render_template('resultados.html', resumenes=[], error = "La fecha de inicio no puede ser posterior a la fecha final.")
            cursor.execute('''
                SELECT 
                    ID,
                    MAX(Cliente),
                    AVG(CASE WHEN Departamento = 'Calidad' THEN CAST(Valor AS FLOAT) END) AS Calidad,
                    AVG(CASE WHEN Departamento = 'Entregas' THEN CAST(Valor AS FLOAT) END) AS Entregas,
                    AVG(CASE WHEN Departamento = 'Servicio' THEN CAST(Valor AS FLOAT) END) AS Servicio,
                    MIN(Fecha) AS FechaEnvio,
                    MAX(Fecha) AS FechaRespuesta
                FROM Respuestas
                WHERE CONVERT(DATE, Fecha) BETWEEN ? AND ?
                GROUP BY ID
                ORDER BY FechaEnvio DESC
            ''',(fecha_inicio, fecha_fin,))
        except ValueError:
            return render_template('resultados.html', resumenes=[], error="Formato de fecha inválido.")
    else:
        cursor.execute('''
            SELECT 
                ID,
                MAX(Cliente),
                AVG(CASE WHEN Departamento = 'Calidad' THEN CAST(Valor AS FLOAT) END) AS Calidad,
                AVG(CASE WHEN Departamento = 'Entregas' THEN CAST(Valor AS FLOAT) END) AS Entregas,
                AVG(CASE WHEN Departamento = 'Servicio' THEN CAST(Valor AS FLOAT) END) AS Servicio,
                MIN(Fecha) AS FechaEnvio,
                MAX(Fecha) AS FechaRespuesta
            FROM Respuestas
            GROUP BY ID
            ORDER BY FechaEnvio DESC
        ''',)

    resumenes = cursor.fetchall()
    resumenes_float = []
    for r in resumenes:
        calidad = float(r[2]) if r[2] is not None else 0.0
        entregas = float(r[3]) if r[3] is not None else 0.0
        servicio = float(r[4]) if r[4] is not None else 0.0
        promedio = round((calidad + entregas + servicio) / 3,2)

        resumenes_float.append((
            r[0],  # ID
            r[1],
            calidad,    
            entregas,
            servicio,
            promedio,
            r[5],  # FechaEnvio
            r[6],  # FechaRespuesta
        ))

    conn.close()
    return render_template('resultados.html', resumenes=resumenes_float)

@app.route('/detalle/<id_encuesta>')
def detalle(id_encuesta):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Respuestas.ID, Respuestas.Cliente, Respuestas.Departamento, Preguntas.Numero, Preguntas.Pregunta, Respuestas.Valor, Respuestas.Fecha
        FROM Respuestas
        INNER JOIN Preguntas ON Respuestas.Pregunta = Preguntas.Numero
        WHERE Respuestas.ID = ?
        ORDER BY CAST(SUBSTRING(Respuestas.Pregunta, 2, LEN(Respuestas.Pregunta)) AS INT), Respuestas.Departamento
    ''', (id_encuesta,))
    resultados = cursor.fetchall()

    cursor.execute(''' 
        SELECT ID, Departamento, Comentarios, Fecha
        FROM Comentarios
        WHERE ID = ?
    ''', (id_encuesta,))
    comentarios = cursor.fetchall()
    conn.close()
    if not resultados:
        return f"No se encontraron resultados para la encuesta {id_encuesta}", 404
    
    return render_template('detalle.html', resultados = resultados, id_encuesta = id_encuesta, comentarios = comentarios)

if __name__ == '__main__':
    app.run(debug=True)
