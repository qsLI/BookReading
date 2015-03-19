#coding:utf-8
import os
from flask import Flask,request,current_app,make_response,redirect,abort,session,url_for
from flask import render_template,send_from_directory,flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


import datetime
app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/',methods=['GET', 'POST'])
def index():
    # user_aget = request.headers.get('User-Agent')
    # response = make_response("<b>It worked!<b><BR>Your browser is %s</p>"%user_aget)
    # response.set_cookie('answer','42')
    # return response
    # return render_template('index.html',current_time=datetime.time())
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/home')
def baidu():
    abort(404)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

if __name__ == "__main__":
    print app.url_map
    app.run(host="192.168.1.189",port=80,debug=True)