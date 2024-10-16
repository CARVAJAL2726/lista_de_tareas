from flask import Flask, render_template
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
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    
    # Verificar si el usuario o contraseña ya existen
    cursor.execute("SELECT * FROM login WHERE users=%s OR passwords=%s", (username, password))
    user = cursor.fetchone()
    
    if user:
        flash('El nombre de usuario o la contraseña ya están en uso. Por favor, elige otros.')
        return redirect(url_for('register'))
    else:
        sql = "INSERT INTO login (users, passwords) VALUES (%s, %s)"
        datos = (username, password)
        cursor.execute(sql, datos)
        conexion.commit()
        flash('Usuario registrado exitosamente.')
    
    return render_template('register.html')


#-----------------login----------------------

@app.route('/login')
def login():
    return render_template('login.html')




@app.route('/templates/login.html' , methods=['POST'] )
def iniciarsecion():
    username= request.form['username']
    password= request.form['password']
    conexion = mysql.connection
    cursor = conexion.cursor()
    sql= "SELECT * FROM login WHERE users = %s AND passwords = %s"
    datos = (username, password)
    cursor.execute(sql,datos)
    conexion.commit()
    ingresar=cursor.fetchone()
    if ingresar:
        return render_template('pagina/pagina.html')
    else:
        flash('Debes registrarte')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug = True)
