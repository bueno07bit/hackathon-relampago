from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Chave secreta para usar sessões

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect("todo.db")  # Cria o arquivo do banco se não existir
    cursor = conn.cursor()

    # Criando a tabela 'tasks'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            done BOOLEAN NOT NULL DEFAULT 0,
            day TEXT NOT NULL
        );      
    """)
    conn.commit()

    # Criando a tabela 'users'
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );  
    """)
    conn.commit()
    conn.close()

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas como dicionários
    return conn

# Rota inicial: Página de registro
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Insere os dados no banco de dados
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for('login'))  # Redireciona para a página de login
        except sqlite3.IntegrityError:
            # Usuário já existe
            return render_template("register.html", error="Usuário já existe!")

    return render_template("register.html")  # Exibe o formulário de cadastro

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verifica o usuário e a senha no banco de dados
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()

        if user:
            # Salva o usuário na sessão
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('add_task'))  # Redireciona para a página de tarefas
        else:
            flash("Usuário ou senha incorretos!", "danger")

    return render_template("login.html")  # Exibe o formulário de login

# Rota para adicionar tarefas
@app.route("/task", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver autenticado

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        day = request.form["day"]

        conn = get_db_connection()
        conn.execute("INSERT INTO tasks (title, description, day) VALUES (?, ?, ?)", (title, description, day))
        conn.commit()
        conn.close()

        return redirect(url_for('add_task'))  # Redireciona para a listagem

    return render_template("index.html")  # Exibe o formulário de adição

# Rota para listar as tarefas
@app.route("/add")
def add_task():
    if "user_id" not in session:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver autenticado

    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY day").fetchall()
    conn.close()
    return render_template("add_task.html", tasks=tasks)

# Rota para marcar a tarefa como concluída
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('add_task'))

# Rota para excluir tarefa
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('add_task'))

# Rota de logout
@app.route("/logout")
def logout():
    session.clear()  # Limpa a sessão
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
