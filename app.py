from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulando banco de dados
students = {
    "1": {"name": "João", "activities": ["Matemática - Redação"], "grades": {"Matemática": 8.5}},
    "2": {"name": "Maria", "activities": ["História - Redação"], "grades": {"História": 9.0}},
    "3": {"name": "Arthur", "activities": ["Ciências - Redação"], "grades": {"Ciências": 8.5}},
    "4": {"name": "Daniel", "activities": ["Geografia- Redação"], "grades": {"Geografia": 7.0}},
    "5": {"name": "Gabriel", "activities": ["Inglês- Redação"], "grades": {"Inglês": 7.5}},
    "6": {"name": "Juliane", "activities": ["Língua Portuguesa - Redação"], "grades": {"Língua Portuguesa": 8.5}},
    "7": {"name": "Bruno", "activities": ["Educação Física - Redação"], "grades": {"Educação Física": 10.0}},
    "8": {"name": "Vitor", "activities": ["Artes - Redação"], "grades": {"Artes": 9.0}},
    "9": {"name": "Vinicius", "activities": ["Ensino Religioso - Redação"], "grades": {"Ensino Religioso": 9.0}},
    
}
courses = ["Matemática", "História", "Ciências", "Geografia", "Inglês","Língua Portuguesa","Educação Física","Artes", "Ensino Religioso"]

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/agenda')
def agenda():
    return render_template('agenda.html', students=students)

@app.route('/atividades')
def atividades():
    return render_template('atividades.html', students=students)

@app.route('/notas')
def notas():
    return render_template('notas.html', students=students)

@app.route('/cursos')
def cursos_page():
    return render_template('cursos.html', courses=courses)

@app.route('/adicionar_estudante', methods=['GET', 'POST'])
def adicionar_estudante():
    if request.method == 'POST':
        student_id = str(len(students) + 1)
        name = request.form['name']
        students[student_id] = {"name": name, "activities": [], "grades": {}}
        return redirect(url_for('index'))
    return render_template('adicionar_estudante.html')

@app.route('/adicionar_nota/<student_id>', methods=['GET', 'POST'])


def adicionar_nota(student_id):
    if request.method == 'POST':
        subject = request.form['subject']
        grade = float(request.form['grade'])
        if subject in students[student_id]['grades']:
            students[student_id]['grades'][subject] = grade
        else:
            students[student_id]['grades'].update({subject: grade})
        return redirect(url_for('notas'))
    return render_template('adicionar_nota.html', student_id=student_id)

@app.route('/adicionar_atividade/<student_id>', methods=['GET', 'POST'])
def adicionar_atividade(student_id):
    if request.method == 'POST':
        activity = request.form['activity']
        students[student_id]['activities'].append(activity)
        return redirect(url_for('atividades'))
    return render_template('adicionar_atividade.html', student_id=student_id)

if __name__ == '__main__':
    app.run(debug=True)
