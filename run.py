from flask import Flask, request, redirect, url_for, render_template, flash,session
from flask import *
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'supersecretkey'

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'lista_de_tareas'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

@app.route('/')
def index():
        return render_template('index.html')
#-------AUTH--------------------
#--------------register------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conexion = mysql.connection
        cursor = conexion.cursor()
        
        # Verificar si el usuario o contraseña ya existen
        cursor.execute("SELECT * FROM login WHERE users=%s OR passwords=%s", (username, password))
        user = cursor.fetchone()
        
        if user:
            flash('El nombre de usuario o la contraseña ya están en uso. Por favor, elige otros.')
            return redirect(url_for('register'))
        else:
            cursor.execute("INSERT INTO login (users, passwords) VALUES (%s, %s)", (username, password))
            conexion.commit()
            flash('Usuario registrado exitosamente.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/templates/register.html', methods=['POST'])
def guardar():
    username = request.form['username']
    password = request.form['password']
    rol = request.form['rol']
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    
    # Verificar si el usuario o contraseña ya existen
    cursor.execute("SELECT * FROM login WHERE users=%s OR passwords=%s ", (username, password))
    user = cursor.fetchone()
    
    if user:
        flash('El nombre de usuario o la contraseña ya están en uso. Por favor, elige otros.')
        return redirect(url_for('register'))
    else:
        sql = "INSERT INTO login (users, passwords,rol) VALUES (%s, %s,%s)"
        datos = (username, password,rol)
        cursor.execute(sql, datos)
        conexion.commit()
        flash(f'Usuario registrado exitosamente como {rol}')
    
    return render_template('register.html')


#-----------------login----------------------

@app.route('/login')
def login():
    return render_template('login.html')




@app.route('/templates/login.html', methods=['POST'])
def iniciarsecion():
    username = request.form['username']
    password = request.form['password']
    conexion = mysql.connection
    cursor = conexion.cursor()
    sql = "SELECT * FROM login WHERE users = %s AND passwords = %s"
    datos = (username, password)
    cursor.execute(sql, datos)
    ingresar = cursor.fetchone()
    
    print(ingresar)  # Imprimir para depuración
    
    if ingresar:
        # Ajustar según los índices correctos de tu tabla login
        session['username'] = ingresar[1]  # Ajusta según sea necesario
        session['rol'] = ingresar[3]  # Ajusta según sea necesario
        if ingresar[3] == 'profesor':
            return redirect(url_for('pagina_profesor'))
        else:
            return redirect(url_for('pagina_estudiante'))
    else:
        flash('Nombre de usuario o contraseña incorrectos.')
        return



#___________pagina del estudiante y profesor________________________________________


@app.route('/pagina_profesor')
def pagina_profesor():
    # Solo accesible para profesores
    if 'rol' in session and session['rol'] == 'profesor':
        return render_template('pagina/pagina_profesor.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/pagina_estudiante')
def pagina_estudiante():
    # Solo accesible para estudiantes
    if 'rol' in session and session['rol'] == 'estudiante':
        return render_template('pagina/pagina_estudiante.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug = True)
