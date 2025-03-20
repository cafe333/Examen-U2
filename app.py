from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/blog_ciberseguridad'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    introduction = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    authors = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        introduction = request.form['introduction']
        year = request.form['year']
        authors = request.form['authors']

        new_article = Article(title=title, introduction=introduction, year=year, authors=authors)
        db.session.add(new_article)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('add_article.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.get_or_404(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.introduction = request.form['introduction']
        article.year = request.form['year']
        article.authors = request.form['authors']

        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_article.html', article=article)

@app.route('/delete/<int:id>')
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

