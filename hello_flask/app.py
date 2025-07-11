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
    return render_template('Generador.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    cliente = request.form['cliente']
    email_calidad = request.form['mailCalidad']
    email_entregas = request.form['mailEntregas']    
    email_servicio = request.form['mailServicio']

    session['cliente'] = cliente

    base_url = "http://localhost:5000"

    asunto_calidad = f"Encuesta de Calidad - {cliente}"
    cuerpo_calidad = f"""
    Estimado cliente {cliente},

    Por favor complete la encuesta de **Calidad** en el siguente enlace:

    {base_url}/Calidad
    
    ¡Gracias por tu tiempo!
    """

    asunto_entregas = f"Encuesta de Entregas - {cliente}"
    cuerpo_entregas = f"""
    Estimado cliente {cliente},

    Por favor complete la encuesta de **Entregas** en el siguente enlace:

    {base_url}/Entregas
    
    ¡Gracias por tu tiempo!
    """

    asunto_servicio = f"Encuesta de Servicio - {cliente}"
    cuerpo_servicio = f"""
    Estimado cliente {cliente},

    Por favor complete la encuesta de **Servicio** en el siguente enlace:

    {base_url}/Servicio
    
    ¡Gracias por tu tiempo!
    """
    enviar_correo(email_calidad, asunto_calidad, cuerpo_calidad)
    enviar_correo(email_entregas, asunto_entregas, cuerpo_entregas)
    enviar_correo(email_servicio, asunto_servicio, cuerpo_servicio)

    flash('Correos enviados con exito')
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
    dep = request.form.get('departamento')
    if dep == 'backCalidad':
        return redirect(url_for('backCalidad'))
    elif dep == 'backEntregas':
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
    return render_template('Calidad.html')

@app.route('/Entregas')
def Entregas():
    return render_template('Entregas.html')

@app.route('/Servicio')
def Servicio():
    return render_template('Servicio.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    cliente = request.form.get('cliente')
    codigo = request.form.get('codigo')
    departamento = request.form.get('dep')
    comentarios = request.form.get('comentarios')

    data = {
        'cliente': cliente,
        'codigo': codigo,
        'departamento': departamento,
        'comentarios': comentarios
    }

    if departamento == 'Calidad':
        data.update({
            'Q1': request.form.get('Q1'),
            'Q2': request.form.get('Q2'),
            'Q3': request.form.get('Q3'),
            'Q4': request.form.get('Q4'),
            'Q5': request.form.get('Q5'),
        })
        
    elif departamento == 'Entregas':
        data.update({
            'Q1': request.form.get('Q1'),
            'Q2': request.form.get('Q2'),
            'Q3': request.form.get('Q3'),
            'Q4': request.form.get('Q4'),
        })

    elif departamento == 'Servicio':
        data.update({
            'Q1': request.form.get('Q1'),
            'Q2': request.form.get('Q2'),
            'Q3': request.form.get('Q3'),
            'Q4': request.form.get('Q4'),
            'Q5': request.form.get('Q5'),
            'Q6': request.form.get('Q6'),
            'Q7': request.form.get('Q7'),
        })

    respuestas.append(data)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Respuestas (
        departamento,
        Q1, Q2, Q3, Q4, Q5, Q6, Q7, comentarios
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        request.form.get('Q1'),
        request.form.get('Q2'),
        request.form.get('Q3'),
        request.form.get('Q4'),
        request.form.get('Q5'),
        request.form.get('Q6'),
        request.form.get('Q7'),
        request.form.get('comentarios')
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
