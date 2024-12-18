from flask import Flask, render_template, request, redirect, url_for
import calendar
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
materias = ["Matemática", "História", "Ciências", "Geografia", "Inglês","Língua Portuguesa","Educação Física","Artes", "Ensino Religioso"]

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/atividades')
def atividades():
    return render_template('atividades.html', students=students)

@app.route('/notas')
def notas():
    return render_template('notas.html', students=students)

@app.route('/materias')
def materias_page():
    return render_template('materias.html', courses=materias)

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

# Dicionário para armazenar a presença dos alunos
presenca = {materia: None for materia in materias}

alunos = ["João", "Maria", "Arthur", "Daniel", "Gabriel", "Juliane", "Bruno", "Vitor", "Vinicius"]

# Dicionário para armazenar a presença (por padrão, todos os alunos estão ausentes)
presenca = {aluno: False for aluno in alunos}

@app.route('/chamada')
def chamada():
    # Passa a lista de alunos e seu status de presença para o template
    return render_template('chamada.html', alunos=alunos, presenca=presenca)

@app.route('/marcar_presenca/<nome>', methods=['POST'])
def marcar_presenca(nome):
    if nome in presenca:
        presenca[nome] = True  # Marca o aluno como presente
    return redirect(url_for('chamada'))

@app.route('/marcar_falta/<nome>', methods=['POST'])
def marcar_falta(nome):
    if nome in presenca:
        presenca[nome] = False  # Marca o aluno como ausente
    return redirect(url_for('chamada'))

@app.route('/adicionar_aluno', methods=['POST'])
def adicionar_aluno():
    novo_aluno = request.form.get('novo_aluno')
    if novo_aluno and novo_aluno not in alunos:
        alunos.append(novo_aluno)  # Adiciona o novo aluno
        presenca[novo_aluno] = False  # Inicializa como ausente
    return redirect(url_for('chamada'))

def gerar_calendario(ano):
    meses = []
    for i in range(1, 13):  # Para cada mês do ano
        # Gera o calendário do mês i do ano especificado
        month_days = calendar.monthcalendar(ano, i)
        meses.append({
            'mes': calendar.month_name[i],
            'dias': month_days
        })
    return meses

@app.route('/calendario')
def calendario():
    # Passa o calendário de 2024 para o template
    ano = 2024
    calendario = gerar_calendario(ano)
    return render_template('calendario.html', ano=ano, calendario=calendario)

if __name__ == '__main__':
    app.run(debug=True)
