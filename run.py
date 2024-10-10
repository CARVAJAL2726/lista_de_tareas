from flask import Flask, render_template
from flask import *
from flask_mysqldb import MySQL



app = Flask(__name__)

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
@app.route('/register')
def register():
    sql= "SELECT * FROM login"
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql)
    login = cursor.fetchall()
    conexion.commit()
    return render_template('register.html', login=login)


@app.route('/templates/register.html' , methods=['POST'] )
def guardar():
    username= request.form['username']
    password= request.form['password']

    sql= "INSERT INTO login (users, passwords) VALUES (%s,%s)"
    datos = (username, password)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug = True)