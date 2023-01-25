from app import app
from app.controllers import home, users, pets

app.secret_key = "SomeSuperSecretKey"


if __name__=="__main__":   
    app.run(debug=True) 