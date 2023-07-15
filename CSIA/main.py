import os
from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
csrf = CSRFProtect(app)
app.config['UPLOAD_FOLDER'] = 'uploads' # folder where uploaded files will be saved
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'ppt', 'pptx', 'doc', 'docx', 'xlsx', 'txt', 'zip'} # allowed file extensions
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # maximum file size allowed is 16 MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# function to check if file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# function to create SQLite connection
def get_db_connection():
    conn = sqlite3.connect('physics_resources.db')
    conn.row_factory = sqlite3.Row
    return conn

# home page
@app.route('/')
def index():
    conn = get_db_connection()
    topics = conn.execute('SELECT * FROM topics').fetchall()
    conn.close()
    return render_template('home.html', topics=topics)

@app.route('/measurements', methods=['GET', 'POST'])
def measurements():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('measurements.html')
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return render_template('measurements.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('measurements.html')
    return render_template('measurements.html')

@app.route('/mechanics')
def mechanics():
    return render_template('mechanics.html')

@app.route('/thermal')
def thermal():
    return render_template('thermal.html')

@app.route('/waves')
def waves():
    return render_template('waves.html')

@app.route('/electricity')
def electricity():
    return render_template('electricity.html')

@app.route('/circular')
def circular():
    return render_template('circular.html')

@app.route('/atomic')
def atomic():
    return render_template('atomic.html')

@app.route('/energy')
def energy():
    return render_template('energy.html')

@app.route('/wave-phenomena')
def wave_phenomena():
    return render_template('wave-phenomena.html')

@app.route('/fields')
def fields():
    return render_template('fields.html')

@app.route('/electromagnetic-induction')
def electromagnetic_induction():
    return render_template('electromagnetic-induction.html')

@app.route('/quantum-and-nuclear-physics')
def quantum_and_nuclear_physics():
    return render_template('quantum-and-nuclear-physics.html')


# topic page
@app.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    conn = get_db_connection()
    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    resources = conn.execute('SELECT * FROM resources WHERE topic_id = ?', (topic_id,)).fetchall()
    conn.close()

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            title = request.form['title']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            conn = get_db_connection()
            conn.execute('INSERT INTO resources (topic_id, title, filename, filepath) VALUES (?, ?, ?, ?)',
                         (topic_id, title, filename, filepath))
            conn.commit()
            conn.close()
        return redirect(url_for('topic', topic_id=topic_id))

    return render_template('topic.html', topic=topic, resources=resources)


# add resource page
@app.route('/add_resource/<int:topic_id>', methods=['GET', 'POST'])
def add_resource(topic_id):
    conn = get_db_connection()
    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        conn = get_db_connection()
        conn.execute('INSERT INTO resources (topic_id, title, url) VALUES (?, ?, ?)',
                     (topic_id, title, url))
        conn.commit()
        conn.close()
        return redirect(url_for('topic', topic_id=topic_id))

    return render_template('add_resource.html', topic=topic)










# import os
# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads' # folder where uploaded files will be saved
# app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'ppt', 'pptx', 'doc', 'docx', 'xlsx', 'txt', 'zip'} # allowed file extensions

# # function to check if file has an allowed extension
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# # function to create SQLite connection
# def get_db_connection():
#     conn = sqlite3.connect('physics_resources.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # home page
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     topics = conn.execute('SELECT * FROM topics').fetchall()
#     conn.close()
#     return render_template('home.html', topics=topics)

# @app.route('/measurements')
# def measurements():
#     return render_template('measurements.html')

# @app.route('/mechanics')
# def mechanics():
#     return render_template('mechanics.html')

# @app.route('/thermal')
# def thermal():
#     return render_template('thermal.html')

# @app.route('/waves')
# def waves():
#     return render_template('waves.html')

# @app.route('/electricity')
# def electricity():
#     return render_template('electricity.html')

# @app.route('/circular')
# def circular():
#     return render_template('circular.html')

# @app.route('/atomic')
# def atomic():
#     return render_template('atomic.html')

# @app.route('/energy')
# def energy():
#     return render_template('energy.html')

# @app.route('/wave-phenomena')
# def wave_phenomena():
#     return render_template('wave-phenomena.html')

# @app.route('/fields')
# def fields():
#     return render_template('fields.html')

# @app.route('/electromagnetic-induction')
# def electromagnetic_induction():
#     return render_template('electromagnetic-induction.html')

# @app.route('/quantum-and-nuclear-physics')
# def quantum_and_nuclear_physics():
#     return render_template('quantum-and-nuclear-physics.html')

# # topic page
# @app.route('/topic/<int:topic_id>')
# def topic(topic_id):
#     conn = get_db_connection()
#     topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
#     resources = conn.execute('SELECT * FROM resources WHERE topic_id = ?', (topic_id,)).fetchall()
#     conn.close()
#     return render_template('topic.html', topic=topic, resources=resources)

# # add resource page
# @app.route('/add_resource/<int:topic_id>', methods=['GET', 'POST'])
# def add_resource(topic_id):
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             conn = get_db_connection()
#             conn.execute('INSERT INTO resources (topic_id, filename, filepath) VALUES (?, ?, ?)',
#                          (topic_id, filename, filepath))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('topic', topic_id=topic_id))
#     else:
#         return render_template('add_resource.html', topic_id=topic_id)

# # SQLite initialization
# def init_db():
#     conn = get_db_connection()
#     with app.open_resource('schema.sql', mode='r') as f:
#         conn.executescript(f.read())
#     conn.close()

# # run SQLite initialization if database doesn't exist
# if not os.path.isfile('physics_resources.db'):
#     init_db()

# if __name__ == '__main__':
#     app.run()
