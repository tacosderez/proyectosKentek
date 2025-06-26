from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'response'

# Simulamos una "base de datos" en memoria
respuestas = []

@app.route('/')
def encuesta():
    return render_template('encuesta.html')

@app.route('/departamento', methods=['POST'])
def departamento():
    nombre = request.form['nombre']
    departamento = request.form['departamento']
    
    session['nombre'] = nombre
    session['departamento'] = departamento

    
    if departamento == 'Calidad':
        return redirect(url_for('Calidad'))
    elif departamento == 'Entregas':
        return redirect(url_for('Entregas'))
    else:
        return redirect(url_for('Servicio'))

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
    nombre = request.form.get('nombre')
    departamento = request.form.get('departamento')
    comentarios = request.form.get('comentarios')

    data = {
        'nombre':nombre,
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
