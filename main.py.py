from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import pyodbc

app = Flask(__name__)
socketio = SocketIO(app)

def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=HospitalDB;Trusted_Connection=yes')
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    print("Database connection verified:", cursor.fetchone())
    return conn, cursor

@app.route('/')
def index():
    return render_template('index.html.html')

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cuarto = request.form.get('cuarto')
        camilla = request.form.get('camilla')
        especialidad = request.form.get('especialidad')
        conn, cursor = get_db_connection()
        id = None
        try:
            cursor.execute("INSERT INTO dbo.Pacientes (Nombre, Cuarto, Camilla, Especialidad) OUTPUT INSERTED.ID VALUES (?, ?, ?, ?)", (nombre, cuarto, camilla, especialidad))
            id = cursor.fetchone()[0]
            conn.commit()
            print("Datos insertados en la base de datos:", id, nombre, cuarto, camilla, especialidad)
        except pyodbc.Error as ex:
            print("Ocurrió un error al intentar insertar los datos:", ex)
        finally:
            conn.close()
        if id is not None:
            socketio.emit('update data', {'ID': id, 'Nombre': nombre, 'Cuarto': cuarto, 'Camilla': camilla, 'Especialidad': especialidad})
            print("Datos enviados a través de Socket.IO:", {'ID': id, 'Nombre': nombre, 'Cuarto': cuarto, 'Camilla': camilla, 'Especialidad': especialidad})
        return redirect(url_for('index'))
    return render_template('ingresar.html')

@socketio.on('delete data')
def handle_delete(data_id):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("DELETE FROM dbo.Pacientes WHERE ID = ?", (data_id,))
        conn.commit()
        print("Datos borrados de la base de datos:", data_id)
    except pyodbc.Error as ex:
        print("Ocurrió un error al intentar borrar los datos:", ex)
    conn.close()

if __name__ == '__main__':
    socketio.run(app)










#  / \__
# (    @\__ 
# / JDMV    O
#/   (_____/
#/1706_/ U
