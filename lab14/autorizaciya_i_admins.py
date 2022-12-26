from table import app, Users,db, tovar, Comments
from flask import render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, RegistrationForm, tovars, CommentForm


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        login = form.login.data
        password = form.password.data
        email = form.email.data

        hash_password = generate_password_hash(password)
        new_user = Users(login=login, password=hash_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    else:
        return render_template('register.html', form=form)


login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global admin

    form = LoginForm()

    if form.validate_on_submit():

        login = form.login.data
        password = form.password.data

        user = Users.query.filter_by(login=login).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                user = Users.query.filter_by(login=login).first()
                admin = user.admin
                return redirect('/')
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def home():
    global c_a
    def check_admin():
        try:
            if admin == True:
                c_a = True
                return c_a
            else:
                c_a = False
                return c_a
        except NameError:
            c_a = None
            return c_a
    c_a = check_admin()


    if request.method=="POST":
        select = request.form.get('comp_select')
        if select == "price":
            a = tovar.query.order_by(tovar.price).all()
        if select == "type1":
            a = tovar.query.filter_by(type='Футболка').all()
        if select == "type2":
            a = tovar.query.filter_by(type='Лонгслив').all()
        if select == "":
            a = tovar.query.order_by(tovar.id).all()
    else:
        a = tovar.query.order_by(tovar.id).all()
    return render_template("home.html", tovar=a, c_a=c_a)



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        description = request.form['description']
        brand = request.form['brand']
        price = request.form['price']
        photo = request.files['photo']

        price = int(price)

        da = tovar(type=type, name=name, description=description, brand=brand, price=price, photo=photo.filename)
        db.session.add(da)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html', form=tovars())


@app.route('/delete/<int:id>/del')
def delete(id):
    u = db.session.get(tovar, id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/')
    
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global admin
    del(admin)
    logout_user()
    return redirect('/')



@app.route('/<int:id>', methods=['GET', 'POST'])
def product_page(id):
    global admin
    b = tovar.query.get(id)
    comments = Comments.query.filter_by(tovar_id=id).all()
    form = CommentForm()

    if form.validate_on_submit():
        like = form.like.data
        comment = form.comment.data

        new_comment = Comments(tovar_id=id, like=like, comment=comment)
        db.session.add(new_comment)
        db.session.commit()
    def check_admin():
        try:
            if admin == True:
                c_a = True
                return c_a
            else:
                c_a = False
                return c_a 
        except NameError:
            c_a = None
            return c_a
    c_a = check_admin()

    return render_template("product.html", c_a = c_a, tovar=b, form=form, comments=comments, )