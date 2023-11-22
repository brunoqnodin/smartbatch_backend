from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Zellda012489@bj'
app.config['MYSQL_DATABASE_DB'] = 'smartbatch'
app.config['MYSQL_DATABASE_HOST'] = 'web.smartgears.com.br'
mysql.init_app(app)
