

from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "ThanksKatie!"
app.config['UPLOAD_FOLDER'] = '/Users/leeloftiss/Desktop/cd/class_files/dec_22_todo_app2/uploads/'