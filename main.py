import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:madyumyum_restaurant_db@localhost:5432/example'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Restaurante(db.Model):
    __tablename__ = 'restaurantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)

    # Relación 1-N: cascade='all, delete-orphan' asegura que al eliminar
    # un restaurante, sus platos se eliminen automáticamente con él.
    platos = db.relationship('Plato', backref='restaurante', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Restaurante id={self.id} nombre={self.nombre}>'

    def format(self):
        """Convierte el objeto Python en un diccionario serializable."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
        }


class Plato(db.Model):
    __tablename__ = 'platos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    # Restricción de verificación para que el precio sea mayor a cero
    precio = db.Column(db.Numeric(10, 2), db.CheckConstraint('precio > 0'), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
    
    # Llave foránea hacia restaurantes.id (con borrado en cascada configurado a nivel de base de datos o SQLAlchemy)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)

    def __repr__(self):
        return f'<Plato id={self.id} nombre={self.nombre}>'

    def format(self):
        """Convierte el objeto Python en un diccionario serializable."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': float(self.precio) if self.precio else 0.0,
            'disponible': self.disponible,
            'restaurante_id': self.restaurante_id,
        }
@app.route('/restaurantes', methods=['GET'])
def listar_restaurantes():
    try:
        ciudad = request.args.get('ciudad')
        consulta = Restaurante.query
        
        if ciudad:
            consulta = consulta.filter(Restaurante.ciudad.ilike(f'%{ciudad}%'))
            
        restaurantes = consulta.order_by(Restaurante.nombre).all()
        return render_template('restaurantes/index.html', restaurantes=restaurantes)
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cargar los restaurantes: {str(e)}', 'error')
        return render_template('errores/500.html'), 500


@app.route('/restaurantes/crear', methods=['GET', 'POST'])
def crear_restaurante():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        ciudad = request.form.get('ciudad')
        direccion = request.form.get('direccion')
        telefonoval = request.form.get('telefono')

        if not nombre or not ciudad:
            flash('El nombre y la ciudad son obligatorios.', 'error')
            return render_template('restaurantes/formulario.html', restaurante=None)

        nuevo_restaurante = Restaurante(
            nombre=nombre,
            ciudad=ciudad,
            direccion=direccion,
            telefono=telefonoval
        )

        try:
            db.session.add(nuevo_restaurante)
            db.session.commit()
            flash('¡Restaurante creado con éxito!', 'success')
            # Patrón Post/Redirect/Get para evitar duplicados con F5
            return redirect(url_for('listar_restaurantes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar en la base de datos: {str(e)}', 'error')
            return render_template('restaurantes/formulario.html', restaurante=None)
        finally:
            db.session.close()

    return render_template('restaurantes/formulario.html', restaurante=None)

@app.route('/restaurantes/<int:restaurante_id>', methods=['GET'])
def detalle_restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if restaurante is None:
        return render_template('errores/404.html'), 404
    return render_template('restaurantes/detalle.html', restaurante=restaurante)


@app.route('/restaurantes/<int:restaurante_id>/editar', methods=['GET', 'POST'])
def editar_restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if restaurante is None:
        return render_template('errores/404.html'), 404

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        ciudad = request.form.get('ciudad')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')

        if not nombre or not ciudad:
            flash('El nombre y la ciudad son obligatorios.', 'error')
            return render_template('restaurantes/formulario.html', restaurante=restaurante)

        restaurante.nombre = nombre
        restaurante.ciudad = ciudad
        restaurante.direccion = direccion
        restaurante.telefono = telefono

        try:
            db.session.commit()
            flash('¡Restaurante actualizado con éxito!', 'success')
            # Post/Redirect/Get hacia el detalle
            return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el restaurante: {str(e)}', 'error')
            return render_template('restaurantes/formulario.html', restaurante=restaurante)
        finally:
            db.session.close()

    return render_template('restaurantes/formulario.html', restaurante=restaurante)

@app.route('/restaurantes/<int:restaurante_id>/eliminar', methods=['POST'])
def eliminar_restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if restaurante is None:
        return render_template('errores/404.html'), 404

    try:
        db.session.delete(restaurante)
        db.session.commit()
        flash('Restaurante y sus platos eliminados correctamente.', 'success')
        return redirect(url_for('listar_restaurantes'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el restaurante: {str(e)}', 'error')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))
    finally:
        db.session.close()

@app.route('/restaurantes/<int:restaurante_id>/platos', methods=['POST'])
def agregar_plato(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if restaurante is None:
        return render_template('errores/404.html'), 404

    nombre = request.form.get('nombre')
    precio_str = request.form.get('precio')
    # Si el checkbox está marcado, llega '1' o 'on', si no, es None
    disponible = True if request.form.get('disponible') else False

    if not nombre or not precio_str:
        flash('El nombre del plato y el precio son obligatorios.', 'error')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))

    try:
        precio = float(precio_str)
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
    except ValueError:
        flash('El precio ingresado no es válido.', 'error')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))

    nuevo_plato = Plato(
        nombre=nombre,
        precio=precio,
        disponible=disponible,
        restaurante_id=restaurante.id
    )

    try:
        db.session.add(nuevo_plato)
        db.session.commit()
        flash('Plato agregado exitosamente.', 'success')
        # Post/Redirect/Get al detalle del restaurante
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar el plato: {str(e)}', 'error')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))
    finally:
        db.session.close()

@app.errorhandler(404)
def no_encontrado(error):
    return render_template('errores/404.html'), 404

@app.errorhandler(500)
def error_interno(error):
    db.session.rollback()
    return render_template('errores/500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
