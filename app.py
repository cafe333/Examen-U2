from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="blog_ciberseguridad"  # Cambié el nombre de la base de datos para coincidir con el original
    )

# Ruta principal: mostrar todos los artículos
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Utilizar dictionary=True para obtener resultados como diccionarios
    cursor.execute("SELECT * FROM article")  # Asegúrate de que la tabla en tu DB sea 'article'
    articles = cursor.fetchall()  # Obtener todos los artículos
    conn.close()
    return render_template('index.html', articles=articles)

# Ruta para agregar un nuevo artículo
@app.route('/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        introduction = request.form['introduction']
        year = request.form['year']
        authors = request.form['authors']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO article (title, introduction, year, authors) VALUES (%s, %s, %s, %s)", 
            (title, introduction, year, authors)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_article.html')

# Ruta para editar un artículo
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM article WHERE id = %s", (id,))
    article = cursor.fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        introduction = request.form['introduction']
        year = request.form['year']
        authors = request.form['authors']

        cursor.execute(
            "UPDATE article SET title = %s, introduction = %s, year = %s, authors = %s WHERE id = %s", 
            (title, introduction, year, authors, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit_article.html', article=article)

# Ruta para eliminar un artículo
@app.route('/delete/<int:id>')
def delete_article(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM article WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


