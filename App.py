from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
from functools import wraps

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'proyecto-base'
mysql = MySQL(app)

# Configuración del servidor
app.secret_key = 'mysecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/ventanaprincipal')
def ventanaprincipal():
    return render_template('ventanaprincipal.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar el usuario
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):  # user[2] es la contraseña cifrada en la base de datos
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('ventanaprincipal'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    hide_navbar = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario ya existe
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()

        if user:
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('register'))
        else:
            # Insertar nuevo usuario con contraseña cifrada
            hashed_password = generate_password_hash(password)
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Usuario registrado con éxito.', 'success')
            return redirect(url_for('login'))

    hide_navbar = True
    return render_template('register.html', hide_navbar=hide_navbar)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']

        # Verificar si el usuario existe en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            return redirect(url_for('change_password', username=username))
        else:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('reset_password'))

    return render_template('reset_password.html')

@app.route('/change_password/<string:username>', methods=['GET', 'POST'])
def change_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)

        # Actualizar la contraseña en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('UPDATE users SET password = %s WHERE username = %s', (hashed_password, username))
        mysql.connection.commit()
        cur.close()

        flash('Contraseña cambiada con éxito.', 'success')
        return redirect(url_for('login'))

    return render_template('change_password.html', username=username)




@app.route('/agregar_funcionario', methods=['GET', 'POST'])
def agregar_funcionario():
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        user_create = session['username']  # Obtener el usuario que inició sesión

        if not identificacion or not nombre or not apellido or not telefono:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('agregar_funcionario'))

        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO funcionarios (identificacion, nombre, apellido, telefono, user_create) VALUES (%s, %s, %s, %s, %s)', 
                        (identificacion, nombre, apellido, telefono, user_create))
            mysql.connection.commit()
            flash('Funcionario agregado satisfactoriamente')
        except MySQLdb.IntegrityError:
            flash('La identificación ya existe. Por favor, ingrese otra.', 'error')
        finally:
            return redirect(url_for('agregar_funcionario'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM funcionarios')
    data = cur.fetchall()
    return render_template('funcionarios.html', funcionarios=data)
       
DEPARTAMENTOS = ["Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío", "Risaralda", "San Andrés y Providencia", "Santander", "Sucre", "Tolima", "Valle del Cauca", "Vaupés", "Vichada"]

@app.route('/agregar_acueducto', methods=['GET', 'POST'])
def agregar_acueducto():
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_acueducto = request.form['nombre']
        ubicacion_acueducto = request.form['ubicacion']
        fecha_analisis = request.form['fecha_analisis']
        ph = request.form['ph']
        clorox = request.form['clorox']
        bacterias = request.form['bacterias']
        descripcion = request.form['descripcion']
        departamento = request.form['departamento']
        identificacion_funcionario = request.form['identificacion_funcionario']
        user_create = session['username']  # Obtener el usuario que inició sesión

        # Verificar que todos los campos requeridos están llenos
        if not nombre_acueducto or not ubicacion_acueducto or not fecha_analisis or not identificacion_funcionario:
            flash('Todos los campos obligatorios deben ser llenados', 'error')
            return redirect(url_for('agregar_acueducto'))

        # Verificar que la identificación del funcionario existe
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM funcionarios WHERE identificacion = %s', (identificacion_funcionario,))
        funcionario = cur.fetchone()

        if not funcionario:
            flash('La identificación del funcionario no existe. Por favor, ingrese una identificación válida.', 'error')
            return redirect(url_for('agregar_acueducto'))

        # Inserta en la base de datos
        try:
            cur.execute("INSERT INTO acueductos (nombre_acueducto, ubicacion_acueducto, fecha_analisis, ph, clorox, bacterias, descripcion, departamento, identificacion_funcionario,  user_create) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (nombre_acueducto, ubicacion_acueducto, fecha_analisis, ph, clorox, bacterias, descripcion, departamento, identificacion_funcionario,  user_create))
            mysql.connection.commit()
            flash('Acueducto agregado correctamente', 'success')
        except MySQLdb.IntegrityError as e:
            flash('Error al agregar el acueducto: {}'.format(e), 'error')
        return redirect(url_for('agregar_acueducto'))

    # Obtener funcionarios y departamentos
    cur = mysql.connection.cursor()
    cur.execute("SELECT identificacion, CONCAT(identificacion, ' / ', nombre) AS nombre_completo FROM funcionarios")
    funcionarios = cur.fetchall()
    # Obtener la lista de acueductos
    cur.execute('SELECT * FROM acueductos')
    acueductos = cur.fetchall()
    
    return render_template('acueductos.html', funcionarios=funcionarios, departamentos=DEPARTAMENTOS, acueductos=acueductos)




@app.route('/editar_acueducto', methods=['GET', 'POST'])
def editar_acueducto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_acueducto, nombre_acueducto FROM acueductos')
    acueductos = cur.fetchall()
    
    if request.method == 'POST':
        acueducto_id = request.form['acueducto_id']
        return redirect(url_for('get_acueducto', id=acueducto_id))
    
    return render_template('editar_acueducto.html', acueductos=acueductos)



@app.route('/get_acueducto/<id>', methods=['GET'])
def get_acueducto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM acueductos WHERE id_acueducto = %s', (id,))
    acueducto = cur.fetchone()
    if not acueducto:
        flash('Acueducto no encontrado', 'error')
        return redirect(url_for('editar_acueducto'))

    # Obtener todos los departamentos
    cur.execute("SELECT DISTINCT departamento FROM acueductos")
    departamentos = cur.fetchall()
    departamentos = [departamento[0] for departamento in departamentos]

    # Obtener todos los funcionarios
    cur.execute("SELECT identificacion, CONCAT(identificacion, ' / ', nombre) AS nombre_completo FROM funcionarios")
    funcionarios = cur.fetchall()

    return render_template('formulario_editar_acueducto.html', acueducto=acueducto, departamentos=DEPARTAMENTOS, funcionarios=funcionarios)

@app.route('/actualizar_acueducto/<id>', methods=['POST'])
def actualizar_acueducto(id):
    if request.method == 'POST':
        nombre_acueducto = request.form['nombre']
        ubicacion_acueducto = request.form['ubicacion']
        fecha_analisis = request.form['fecha_analisis']
        ph = request.form['ph']
        clorox = request.form['clorox']
        bacterias = request.form['bacterias']
        descripcion = request.form['descripcion']
        departamento= request.form['departamento']
        identificacion_funcionario = request.form['identificacion_funcionario']
        user_update = session['username']  # Obtener el usuario que inició sesión

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE acueductos
        SET nombre_acueducto = %s,
            ubicacion_acueducto = %s,
            fecha_analisis = %s,
            ph = %s,
            clorox = %s,
            bacterias = %s,
            descripcion = %s,
            departamento = %s,
            identificacion_funcionario = %s,
            user_update = %s
        WHERE id_acueducto = %s
        """, (nombre_acueducto, ubicacion_acueducto, fecha_analisis, ph, clorox, bacterias, descripcion, departamento, identificacion_funcionario, user_update, id))
        mysql.connection.commit()
        flash('Acueducto editado exitosamente')
        return redirect(url_for('agregar_acueducto'))

@app.route('/editar_funcionario', methods=['GET', 'POST'])
def editar_funcionario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, identificacion, nombre, apellido, telefono FROM funcionarios')
    funcionarios = cur.fetchall()
    
    if request.method == 'POST':
        id_funcionario = request.form['identificacion']  # Asegúrate de que este nombre coincide con el campo en tu formulario HTML
        return redirect(url_for('get_funcionario', id=id_funcionario))
    
    return render_template('editar_funcionario.html', funcionarios=funcionarios)

@app.route('/get_funcionario/<id>', methods=['GET'])
def get_funcionario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM funcionarios WHERE id = %s', (id,))
    funcionario = cur.fetchone()
    if not funcionario:
        flash('Funcionario no encontrado', 'error')
        return redirect(url_for('editar_funcionario'))
    return render_template('formulario_editar_funcionario.html', funcionario=funcionario)

@app.route('/actualizar_funcionario', methods=['POST'])
def actualizar_funcionario():
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        nueva_identificacion = request.form['nueva_identificacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        user_update = session['username']  # Obtener el usuario que inició sesión

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE funcionarios
            SET identificacion = %s,
                nombre = %s,
                apellido = %s,
                telefono = %s,
                user_update = %s  -- Actualizar el usuario que realizó la actualización
            WHERE id = %s
            """, (nueva_identificacion, nombre, apellido, telefono, user_update, identificacion))
            mysql.connection.commit()
            flash('Funcionario actualizado exitosamente')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al actualizar el funcionario: {str(e)}', 'error')
        finally:
            return redirect(url_for('agregar_funcionario'))

@app.route('/eliminar_funcionario', methods=['GET', 'POST'])
def eliminar_funcionario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT identificacion, CONCAT(nombre, " ", apellido) AS nombre_completo FROM funcionarios')
    funcionarios = cur.fetchall()
    
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        
        # Verificar si el funcionario está asociado a algún acueducto
        cur.execute('SELECT * FROM acueductos WHERE identificacion_funcionario = %s', (identificacion,))
        acueducto = cur.fetchone()
        
        if acueducto:
            flash('Este funcionario está asociado a un acueducto. Elimina el acueducto primero.', 'error')
            # Si el funcionario está asociado a un acueducto, mostrar la alerta de error y redirigir
            return redirect(url_for('eliminar_funcionario'))
        
        # Si el funcionario no está asociado a ningún acueducto, proceder con la eliminación
        cur.execute('DELETE FROM funcionarios WHERE identificacion = %s', (identificacion,))
        mysql.connection.commit()
        flash('Funcionario eliminado exitosamente', 'success')
        # Si se eliminó correctamente, mostrar mensaje de éxito
        
        return redirect(url_for('eliminar_funcionario'))

    return render_template('eliminar_funcionario.html', funcionarios=funcionarios)

@app.route('/eliminar_acueducto', methods=['GET', 'POST'])
def eliminar_acueducto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_acueducto, nombre_acueducto FROM acueductos')
    acueductos = cur.fetchall()
    
    if request.method == 'POST':
        id_acueducto = request.form['id_acueducto']
        cur.execute('DELETE FROM acueductos WHERE id_acueducto = %s', (id_acueducto,))
        mysql.connection.commit()
        flash('Acueducto eliminado exitosamente')
        return redirect(url_for('eliminar_acueducto'))

    return render_template('eliminar_acueducto.html', acueductos=acueductos)




@app.route('/acueductos_por_departamento')
def acueductos_por_departamento():
    departamento = request.args.get('departamento')
    ##print('Departamento:', departamento)  # Mensaje de depuración
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM acueductos WHERE departamento = %s', (departamento,))
    result = cur.fetchone()
    ##print('Resultado de la consulta:', result)  # Mensaje de depuración
    return jsonify({'num_acueductos': result[0]})

@app.route('/promedio_acueducto_por_departamento')
def promedio_acueducto_por_departamento():
    departamento = request.args.get('departamento')
    cur = mysql.connection.cursor()
    cur.execute('SELECT AVG(ph), AVG(clorox), AVG(bacterias) FROM acueductos WHERE departamento = %s', (departamento,))
    result = cur.fetchone()
    # Redondear los valores a dos decimales y devolver 0 si es None
    promedio_ph = round(result[0], 2) if result[0] is not None else 0
    promedio_clorox = round(result[1], 2) if result[1] is not None else 0
    promedio_bacterias = round(result[2], 2) if result[2] is not None else 0
    return jsonify({'promedio_ph': promedio_ph, 'promedio_clorox': promedio_clorox, 'promedio_bacterias': promedio_bacterias})






if __name__ == '__main__':
    app.run(port=3000, debug=True)


