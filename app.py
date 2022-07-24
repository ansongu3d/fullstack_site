import os
import psycopg2
from flask import Flask


# get DATABASE_URL value from environment,
# if the value is NOT found, then use 'dbname=food_truck'
DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=foodtruck')

# get SECRET_KEY value from environment,
# if the value is NOT found, then use 'bambi-thumper-example'
#
# Tip:
# 
# You can use the following code snippet to generate random secret key for your production environment
#   import secrets
#   secrets.token_hex(16)
SECRET_KEY = os.environ.get('SECRET_KEY', 'bambi-thumper-example')

app = Flask (__name__)
app.secret_key = SECRET_KEY.encode()

@app.route('/')
def index():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    connection.close()
    return '<h1>hello, world</h1>'

if __name__ == "__main__":
    app.run(debug=True)