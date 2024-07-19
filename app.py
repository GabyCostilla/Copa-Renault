import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos usando las variables de entorno o valores específicos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ujxh8tptugv44iuc:qoXCN3J0dH8sLBx9iSKU@bdmhskhmd2zuhryobzdq-mysql.services.clever-cloud.com:3306/bdmhskhmd2zuhryobzdq'
app.config['SECRET_KEY'] = 'qoXCN3J0dH8sLBx9iSKU'  # Clave secreta para proteger formularios

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importa las clases después de inicializar db
from models import Team, Product, ContactMessage, User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas y lógica de la aplicación
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/fixture')
def fixture():
    return render_template('fixture.html')

@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    from forms import RegistrationForm  # Importación local para evitar circularidad
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('inscripcion.html', form=form)

@app.route('/cantina', methods=['GET', 'POST'])
def cantina():
    from forms import PurchaseForm  # Importación local para evitar circularidad
    form = PurchaseForm()
    try:
        products = Product.query.all()
        if form.validate_on_submit():
            product_id = form.product_id.data
            quantity = form.quantity.data
            # Lógica para procesar la compra
            flash('¡Compra realizada con éxito!', 'success')
            return redirect(url_for('home'))
        return render_template('cantina.html', form=form, products=products)
    except Exception as e:
        print(f"Error en /cantina: {e}")
        return "Error interno del servidor", 500

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        image_url = request.form['image_url']
        price = request.form['price']
        
        new_product = Product(name=name, image_url=image_url, price=price)
        db.session.add(new_product)
        db.session.commit()
        
        flash('¡Producto agregado exitosamente!', 'success')
        return redirect(url_for('cantina'))
    
    return render_template('add_product.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    from forms import ContactForm  # Importación local para evitar circularidad
    form = ContactForm()
    if form.validate_on_submit():
        new_message = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_message)
        db.session.commit()
        flash('¡Mensaje enviado exitosamente!', 'success')
        return redirect(url_for('home'))
    return render_template('contacto.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm  # Importación local para evitar circularidad
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('¡Nombre de usuario o contraseña incorrectos!', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Sesión cerrada correctamente!', 'success')
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signin():
    from forms import RegistrationForm  # Importación local para evitar circularidad
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
