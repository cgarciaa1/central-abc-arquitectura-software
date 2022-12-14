from base import app, api, ma, r, Resource, Flask, request



class SignalPublisherResource(Resource):

    def post(self):
        
        #name=
        message = str({'evento' : str(request.json['evento']), 'datos' : str(request.json['datos']), 'hash' : str(request.json['hash']) })
        r.publish('signal-channel', message)
        return {"status":"Ok", "response": "Mensaje publicado"}, 200

api.add_resource(SignalPublisherResource, '/api-commands/signals')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')