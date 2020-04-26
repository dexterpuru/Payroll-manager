import os

SECRET_KEY = os.urandom(32)

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:puru2000@localhost/payroll"

USERNAME = 'dexterpuru'

PASSWORD = 'helloworld'

PAYROLL_STATUS = False
