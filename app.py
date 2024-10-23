from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta'  

def generar_id_unico():
    if 'productos' not in session or len(session['productos']) == 0:
        return 1
    else:
        return max([producto['id'] for producto in session['productos']]) + 1

@app.route('/')
def index():
    productos = session.get('productos', [])  
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': generar_id_unico(),
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'categoria': request.form['categoria']
        }
        
        if 'productos' not in session:
            session['productos'] = []
        session['productos'].append(nuevo_producto)
        session.modified = True 

        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    productos = session.get('productos', [])
    session['productos'] = [producto for producto in productos if producto['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session.get('productos', [])
    producto = next((prod for prod in productos if prod['id'] == id), None)
    
    if request.method == 'POST':
        if producto:
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = int(request.form['cantidad'])
            producto['precio'] = float(request.form['precio'])
            producto['categoria'] = request.form['categoria']
            session.modified = True

        return redirect(url_for('index'))
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
