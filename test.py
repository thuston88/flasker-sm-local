from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class MyForm(FlaskForm):
    username = StringField('Name')
    password = StringField('Password')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()

    if form.validate_on_submit():
        # Process form data
        username = form.username.data
        password = form.password.data
        # Perform desired actions with the form data

        return f'Thank you for submitting the form, {username}!'

    return render_template('E_login.html', form=form)

@app.route('/option', methods=['GET', 'POST'])
def option():
    return render_template('E_option.html')

@app.route('/select', methods=['GET', 'POST'])
def select():
    return render_template('E_select.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('E_add.html')

if __name__ == '__main__':
    app.run(debug=True)

