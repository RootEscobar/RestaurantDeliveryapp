from restaurant import app, api
from flask import render_template, redirect, url_for, flash, request, session, Response
from restaurant.models import Table, User, Item, Order
from restaurant.forms import RegisterForm, LoginForm, OrderIDForm, ReserveForm, AddForm, OrderForm
from restaurant import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
#PAGINA PRINCIPAL
@app.route('/home')
def home_page(): 
    return render_template('index.html')

#PAGINA DEL MENU
@app.route('/menu', methods = ['GET', 'POST'])
@login_required
def menu_page():
    add_form = AddForm()
    if request.method == 'POST':
        selected_item = request.form.get('selected_item') #Obtener el elemento seleccionado de la página del menú
        s_item_object = Item.query.filter_by(name = selected_item).first()
        if s_item_object:
            s_item_object.assign_ownership(current_user) #Asignar la propiedad del artículo pedido al usuario.
        
        return redirect(url_for('menu_page'))
    
    if request.method == 'GET':
        items = Item.query.all()
        return render_template('menu.html', items = items, add_form = add_form)

#PAGINA DEL MENU
@app.route('/cart', methods = ['GET', 'POST'])
def cart_page():
    order_form = OrderForm()
    if request.method == 'POST':
        ordered_item = request.form.get('ordered_item') #Obtiene los artículos pedidos desde la página del carrito
        o_item_object = Item.query.filter_by(name = ordered_item).first()
        order_info = Order(name = current_user.fullname,
                           address = current_user.address,
                           order_items = o_item_object.name ) 

        db.session.add(order_info)
        db.session.commit()

        o_item_object.remove_ownership(current_user)    
        #Regresar a la página de felicitaciones por el pedido realizado con éxito
        return redirect(url_for('congrats_page'))
    
    if request.method == 'GET':
        selected_items = Item.query.filter_by(orderer = current_user.id)#Obtener elementos que el usuario ha añadido al carrito
        return render_template('cart.html', order_form = order_form, selected_items = selected_items)

#PAGINA DE FELICITACIONES POR EL PEDIDO
@app.route('/congrats')
def congrats_page():
    return render_template('congrats.html')   

#PAGINA DE RESERVACION DE MESA
@app.route('/table', methods = ['GET', 'POST'])
@login_required
def table_page():
    reserve_form = ReserveForm()
    #Para deshacerse de 'confirmar reenvío de formulario' al actualizar
    if request.method == 'POST':
        reserved_table = request.form.get('reserved_table')
        r_table_object = Table.query.filter_by(table = reserved_table).first()
        if r_table_object:
            r_table_object.assign_ownership(current_user) #Establezca el propietario de la tabla en el usuario que ha iniciado sesión actualmente
            # flash(f"Your table {{ r_table_object.table }} has been reserved successfully!")

        return redirect(url_for('table_page'))

    if request.method == 'GET':
        tables = Table.query.filter_by(reservee = None)
        return render_template('table.html', tables = tables, reserve_form = reserve_form)

#PAGINA DE INICIO DE SESION
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    forml = LoginForm()
    form = RegisterForm()
    if forml.validate_on_submit():
        attempted_user = User.query.filter_by(username = forml.username.data).first() #Obtener los datos del nombre de usuario ingresados ​​desde el formulario de inicio de sesión
        if attempted_user and attempted_user.check_password_correction(attempted_password = forml.password.data): #Para comprobar si el nombre de usuario y la contraseña ingresados ​​están en la base de datos de usuarios
            login_user(attempted_user) #Comprueba si el usuario está registrado
            # flash(f'Signed in successfully as: {attempted_user.username}', category = 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password is incorrect! Please Try Again', category = 'danger') #Aparece en caso de que el usuario no esté registrado.
    return render_template('login.html', forml = forml, form = form)

#PERDIDA DE CONTRASEÑA
@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    return render_template("forgot.html")

def return_login():
    return render_template("login.html")


#CERRAR SESIÓN
@app.route('/logout')
def logout():
    logout_user() #utilizado para cerrar sesión
    flash('You have been logged out!', category = 'info')
    return redirect(url_for("home_page")) 

#PAGINA DE RESGRITRARSE
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    forml = LoginForm()
    form = RegisterForm() 
    #Comprueba si el formulario es válido
    if form.validate_on_submit():
         user_to_create = User(username = form.username.data,
                               fullname = form.fullname.data,
                               address = form.address.data,
                               phone_number = form.phone_number.data,
                               password = form.password1.data,)
         db.session.add(user_to_create)
         db.session.commit()
         login_user(user_to_create) #Inicie sesión como usuario en el registro
         return redirect(url_for('verify'))
    # else:
    #     flash("Username already exists!")

    if form.errors != {}: #Si no hay errores de las validaciones
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('login.html', form = form, forml = forml)

#PAGINA DE ID DE PEDIDO
@app.route('/order_id', methods = ['GET', 'POST'])
def track_page():
    orderid = OrderIDForm()
    # if request.method == "POST":
    if orderid.validate_on_submit:
        #Verifique si el ID del pedido coincide
        valid_orderid = Order.query.filter_by( order_id = orderid.orderid.data ).first()
        if valid_orderid:
            return redirect(url_for('delivery'))
        else:
            flash('Your Order-ID is invalid! Please Try Again.', category = 'danger')

    return render_template('order-id.html', orderid = orderid)

#PÁGINA DE SEGUIMIENTO DE ENTREGA
@app.route('/deliverytracking')
def delivery():
    return render_template('track.html')

#VERIFICACION OTP
@app.route("/verify", methods=["GET", "POST"])
def verify():
    country_code = "+503"
    phone_number = current_user.phone_number
    method = "sms"
    session['country_code'] = "+503"
    session['phone_number'] = current_user.phone_number

    api.phones.verification_start(phone_number, country_code, via=method)

    if request.method == "POST":
            token = request.form.get("token") #Usuario OTP ingresado

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                # return Response("<h1>Your Phone has been Verified successfully!</h1>")
                return render_template("index.html")
            else:
                # return Response("<center><h1>Wrong OTP!</h1><center>")
                flash('Your OTP is incorrect! Please Try Again', category = 'danger')

    return render_template("login.html")


