from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from webforms import LoginForm, UserForm, SearchForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, fresh_login_required
# from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

from rich.console import Console
from rich.table import Table
from rich import print

# Create a Flask Instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estate.db'

# Secret Key!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

# Initialize The Database
db = SQLAlchemy(app)

# db.init_app(app)

# migrate = Migrate(app, db)

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.username

# Create Model
class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(30), nullable=False)
    acct_type = db.Column(db.String(20))
    acct_number = db.Column(db.String(20), unique=True)
    acct_balance = db.Column(db.String(20))
    access_type = db.Column(db.String(20))
    access_app = db.Column(db.String(30))
    acct_id = db.Column(db.String(20))
    acct_pw = db.Column(db.String(20))
    comment = db.Column(db.String(100))
    extra = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'E_login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Pass Stuff To Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

####################################

# Create Admin Page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry you must be the Admin to access the Admin Page...")
        return redirect(url_for('dashboard'))


# Create Search Function
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the Database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("search.html",
         form=form,
         searched = post.searched,
         posts = posts)


# logout user on init
def init_app():
    logout_user()

"""
# SAVED

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(f'user name on form: {form.username.data}')
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        print(f'user retrieved: {user}')
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfull!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")

    flash("Form is not validated")
    return render_template("E_login.html", form=form)
"""
# this is for testing only
#
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print(f'user name on form: {form.username.data}')

        user = Users.query.filter_by(username=form.username.data).first()

        # for row in user:
        #    print(f' username: {row.username} -  password: {row.password_hash}')

        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfull!!")
                return redirect(url_for('option'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")

    else:
        print("form did not validate")
        print(f'user name on form: {form.username.data}')

        user = Users.query

        for row in user:
            print(f' username: {row.username} -  password: {row.password_hash}')


    # flash("Form is not validated")
    return render_template("E_login.html", form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for('login'))

##########################
# New E- roiutes
##########################

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id or id == 14:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # Return a message
            flash("Blog Post Was Deleted!")

            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)


        except:
            # Return an error message
            flash("Whoops! There was a problem deleting post, try again...")

            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        # Return a message
        flash("You Aren't Authorized To Delete That Post!")

        # Grab all the posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

@app.route('/posts')
def posts():
    # Grab all the posts from the database
    posts = Assets.query.order_by(Assets.id)
    # table of assets
    table = Table(title="Assets")

    table.add_column("Id", justify="right", style="cyan", no_wrap=True)
    table.add_column("Institution", justify="right", style="cyan", no_wrap=True)
    table.add_column("Account Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Account No", justify="right", style="cyan", no_wrap=True)
    table.add_column("Account Bal", justify="right", style="cyan", no_wrap=True)
    table.add_column("Access Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Access App", justify="right", style="cyan", no_wrap=True)
    table.add_column("User Id", justify="right", style="cyan", no_wrap=True)
    table.add_column("Password", justify="right", style="cyan", no_wrap=True)
    table.add_column("Comment", justify="right", style="cyan", no_wrap=True)
    table.add_column("Extra", justify="right", style="cyan", no_wrap=True)

    for p in posts:
        sid = str(p.id)
        table.add_row(sid, p.institution, p.acct_type, p.acct_number, p.acct_balance, p.access_type, p.access_app, p.acct_id, p.acct_pw, p.comment, p.extra)

    console = Console()
    console.print(table)

    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        #post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('post', id=post.id))
    
    if current_user.id == post.poster_id or current_user.id == 14:
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You Aren't Authorized To Edit This Post...")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
        # Clear The Form
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Blog Post Submitted Successfully!")

    # Redirect to the webpage
    return render_template("add_post.html", form=form)

##########################
# posts
##########################


@app.route('/option', methods=['GET', 'POST'])
def option():
    return render_template('E_option.html')


@app.route('/select', methods=['GET', 'POST'])
@login_required
def select():
    form = SelectForm()

    if form.validate_on_submit():

        institution = form.institution.data
        if institution == "choose":
            institution = "*"

        accttype = form.accttype.data
        if accttype == "choose":
            accttype = "*"

        acctno = form.acctno.data
        if acctno == "choose":
            acctno = "*"

        rec_id = Assets.query.filter_by(institution=institution, acct_type=accttype, acct_no=acctno).first()

    asset = Assets.query

    instits =0

    accttype =0

    acctno =0

    return render_template('E_select-test.html',
                           form=form,
                           instits=instits,
                           accttype=accttype,
                           acctno=acctno)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    return render_template('E_add.html')

@app.route('/all', methods=['GET', 'POST'])
@login_required
def all():
    return render_template('E_option.html')

@app.route('/correct', methods=['GET', 'POST'])
@login_required
def correct():
    return render_template('E_option.html')

@app.route('/remove', methods=['GET', 'POST'])
@login_required
def remove():
    return render_template('E_option.html')


# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.username = request.form['username']

        # Check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files['profile_pic']

            # Change it to a string to save to db
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully!")
                return render_template("dashboard.html",
                    form=form,
                    name_to_update = name_to_update)
            except:
                flash("Error!  Looks like there was a problem...try again!")
                return render_template("dashboard.html",
                    form=form,
                    name_to_update = name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html",
                form=form,
                name_to_update = name_to_update)
    else:
        return render_template("dashboard.html",
                form=form,
                name_to_update = name_to_update,
                id = id)

    return render_template('dashboard.html')


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    # Check logged in id vs. id to delete
    if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!!")

            our_users = Users.query.order_by(Users.name)
            return render_template("add_user.html",
            form=form,
            name=name,
            our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, try again...")
            return render_template("add_user.html",
            form=form, name=name,our_users=our_users)
    else:
        flash("Sorry, you can't delete that user! ")
        return redirect(url_for('dashboard'))


# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                form=form,
                name_to_update = name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("update.html",
                form=form,
                name_to_update = name_to_update,
                id=id)
    else:
        return render_template("update.html",
                form=form,
                name_to_update = name_to_update,
                id = id)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    username = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            # username not found
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "scrypt")
            user = Users(username=form.username.data,  password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ''
        form.password_hash.data = ''

        flash("User Added Successfully!")
    else:
        flash("Not Registered Yet")

    our_users = Users.query.order_by(Users.username)
    for row in our_users:
        # print(row)
        print(row.id, row.username, row.password_hash)

    print(f'our_users: {our_users}')
    print(f'username: {username}')
    print(f'type of our_users: {type(our_users)}')

    return render_template("E-adduser.html",
        form=form,
        username=username,
        our_users=our_users)


# Create a route decorator
def index():
    init_app()
    first_name = "Tom"
    stuff = "This is bold text"

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html",
        first_name=first_name,
        stuff=stuff,
        favorite_pizza = favorite_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()


    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # Lookup User By Email Address
        pw_to_check = Users.query.filter_by(email=email).first()

        # Check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html",
        email = email,
        password = password,
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)


