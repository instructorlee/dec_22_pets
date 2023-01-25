from app import app
from app.controllers import home, users, pets
from app.api_controllers import users, pets

app.secret_key = "SomeSuperSecretKey"


if __name__=="__main__":   
    app.run(debug=True) 