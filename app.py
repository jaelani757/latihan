from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_len'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'file')  # Folder untuk menyimpan file yang diupload
db = SQLAlchemy(app)

class Presentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    # kategori = db.column(db.Enum('Internal', 'External'))
    # tanggal = db.column(db.date, nullable=False)
    # event = db.column(db.string(255), nullable=False)
    # tag =  db.column(db.string(255),nullable=False)
    local_link = db.Column(db.String(255), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Simpan file ke folder uploads
        return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    with app.app_context():
        if request.method == 'POST':
            keyword = request.form['keyword']
            results = Presentation.query.filter(Presentation.keyword.like(f"%{keyword}%")).all()
            unique_results = []
            displayed_entries = set()
            for result in results:
                entry = (result.title, result.page_number)
                if entry not in displayed_entries:
                    unique_results.append(result)
                    displayed_entries.add(entry)
            return render_template('results.html', results=unique_results, keyword=keyword)
        else:
            return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
