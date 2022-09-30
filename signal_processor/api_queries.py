from base import app, api, ma, r, Resource, Flask, request
import time
import threading
import json
import hashlib
import logging

key = "12345678910"
requests= 0
errors = 0
status= "OK"

subcription = r.pubsub()    
subcription.subscribe("signal-channel") 

class SignalProcessorResource(Resource):

    def get(self):
        global requests
        global errors
        global status
        return {"status": status, "number_errors": errors, "number_messages": requests }, 200

api.add_resource(SignalProcessorResource, '/api-queries/signals')


def thread_function(p):
    global errors
    global requests
    global key

    while True:
        try:
            message = subcription.get_message()
            logging.warning("Mensaje entrante: {}".format(message))
            if message and "data" in message :    
                logging.warning("Entró mensaje: {}".format(message))
                
                json_object = json.loads(str(message["data"]).replace('\'', '"'))
                if "datos" in json_object:
                    requests += 1
                    hash = hashlib.sha512(str(json_object["datos"] + key).encode("utf-8")).hexdigest()
                    if hash != json_object["hash"]:
                        errors += 1
        except Exception as e: 
            logging.warning("Error capturado: {}".format(e), exc_info=True))                
        time.sleep(3)


if __name__ == '__main__':
  
    x = threading.Thread(target=thread_function, args=(0,))
    x.start()

    app.run(debug=True, host='0.0.0.0')