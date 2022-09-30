from base import app, api, Resource, request
from model import *
from flask_jwt_extended import JWTManager, create_access_token

class AuthenticationResource(Resource):
    def __init__(self, monitor):
        self.__login_monitor__ = monitor       
        super().__init__()

    def post(self):
        username=request.json['username']
        password=request.json['password']
        if self.__login_monitor__.authenticate_user(username, password):
            token_de_acceso = create_access_token(identity=username)
            return {"status":"Authenticated", "JWT": token_de_acceso}, 200
        return {"status":"Error", "response": "Usuario y/o contraseña invalido(s)"}, 401

    def get(self):
        return self.__login_monitor__.getMetrics()


if __name__ == '__main__':
    # monitor configuration
    MAX_USER_LOGIN_ATTEMPS = 3
    
    # data setup
    admin_user = User("admin", "supersecret", LoginTracker())
    sensor1_user = User("sensor_1", "sensor1", LoginTracker())
    monitor = LoginMonitor([admin_user, sensor1_user], MAX_USER_LOGIN_ATTEMPS)

    # endpoint handlers
    api.add_resource(AuthenticationResource, '/api-commands/authenticate', resource_class_kwargs={'monitor': monitor})

    # security
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    JWTManager(app)
    # app run
    app.run(debug=True, host='0.0.0.0')