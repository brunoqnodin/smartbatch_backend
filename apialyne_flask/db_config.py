from app import app
from flask_mysqldb import MySQL


# MySQL configurations
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Alyne2023!@#'
app.config['MYSQL_DB'] = 'smartbatch'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)
