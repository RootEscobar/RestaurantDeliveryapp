from wtforms.validators import Length
from restaurant import db, login_manager
from restaurant import bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func

#Se utiliza para iniciar sesión de usuarios.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#tabla usuarios
class User(db.Model, UserMixin):
    #Considere cambiar id a user_id
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    fullname = db.Column(db.String(length = 30), nullable = False)
    address = db.Column(db.String(length = 50), nullable = False)
    phone_number = db.Column(db.Integer(), nullable = False)
    password_hash = db.Column(db.String(length = 60), nullable = False)

    tables = db.relationship('Table', backref = 'reserved_user', lazy = True) # relación con 'Table'
    items = db.relationship('Item', backref = 'ordered_user', lazy = True) # relación con 'Item'
    orders = db.relationship('Order', backref = 'order-id_user', lazy = True) #relación con 'Table')

    @property
    def password(self):
        return self.password
    
    #hashea la contraseña del usuario
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    #verifica si la contraseña ingresada en el formulario de inicio de sesión coincide con la contraseña del usuario en la base de datos
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
#TABLA RESERVACION DE MESA
class Table(db.Model):
    #Considere cambiar id a table_id
    table_id = db.Column(db.Integer(), primary_key = True)
    table = db.Column(db.Integer(), nullable = False)
    time = db.Column(db.String(length = 20), nullable = False)
    date = db.Column(db.String(length = 20), nullable = False)
    accomodation = db.Column(db.Integer(), nullable = False)
    #Sugerencia: es posible que quieras cambiar 'owner' DE 'reservee'
    reservee = db.Column(db.String(), db.ForeignKey('user.id'))  #Se utiliza para almacenar información sobre la mesa reservada del usuario.

    #Función para asignar propiedad a la tabla reservada del usuario.
    def assign_ownership(self, user):
        self.reservee = user.fullname 
        db.session.commit()

#TABLA MENU
class Item(db.Model):
    #considere cambiar la identificación a item_id
    item_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False)
    description = db.Column(db.String(length = 50), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    source = db.Column(db.String(length = 30), nullable = False)
    #Sugerencia: es posible que quieras cambiar 'owner' to 'orderer'/ 'customer'
    orderer = db.Column(db.Integer(), db.ForeignKey('user.id'))  #Se utiliza para almacenar información sobre el artículo pedido por el usuario.

    #Función para asignar propiedad al elemento seleccionado por el usuario.
    def assign_ownership(self, user):
        self.orderer = user.id 
        db.session.commit()

    def remove_ownership(self, user):
        self.orderer = None
        db.session.commit()



#TABLA
class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), db.ForeignKey('user.username'))
    address = db.Column(db.String(length = 30), nullable = False)
    order_items = db.Column(db.String(length = 300), nullable = False)
    datetime = db.Column(db.DateTime(timezone = True), server_default = func.now())

 
#CART TABLE



