from flask import Flask


app = Flask(__name__)
#add a SECRET_KEY to the app config
app.config['SECRET_KEY'] = 'you-will-never-ever-EVER-gain-access'


from . import routes