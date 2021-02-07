from flask import Flask


# Création app
app = Flask(__name__)

from . import views