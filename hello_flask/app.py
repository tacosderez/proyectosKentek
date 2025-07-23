import pyodbc
from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib
from email.message import EmailMessage
from datetime import datetime
import random

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

# Simulamos una "base de datos" en memoria
respuestas = []

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

    # Adjuntamos el link a cada mensaje manual
    cuerpo_calidad += f"\n\nCompleta la encuesta aquí:\n{base_url}/Calidad?cliente={cliente}&id={codigo_final}"
    cuerpo_entregas += f"\n\nCompleta la encuesta aquí:\n{base_url}/Entregas?cliente={cliente}&id={codigo_final}"
    cuerpo_servicio += f"\n\nCompleta la encuesta aquí:\n{base_url}/Servicio?cliente={cliente}&id={codigo_final}"

    enviar_correo(email_calidad, asunto_calidad, cuerpo_calidad)
    enviar_correo(email_entregas, asunto_entregas, cuerpo_entregas)
    enviar_correo(email_servicio, asunto_servicio, cuerpo_servicio)

    flash('Correos enviados con éxito')
    return redirect(url_for('generador'))


def enviar_correo(destinario, asunto, cuerpo):
    remitente = "jqnterrazas@gmail.com"
    password = "kvyd zida utla rhrd" 

    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinario
    msg.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
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
    cliente = request.args.get('cliente')
    codigo_final = request.args.get('id')
    return render_template('Calidad.html',cliente=cliente, codigo_final=codigo_final)

@app.route('/Entregas')
def Entregas():
    cliente = request.args.get('cliente')
    codigo_final = request.args.get('id')
    return render_template('Entregas.html',cliente=cliente, codigo_final=codigo_final)

@app.route('/Servicio')
def Servicio():
    cliente = request.args.get('cliente')
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

@app.route('/resultados')
def resultados():
    return {'respuestas': respuestas}

if __name__ == '__main__':
    app.run(debug=True)
