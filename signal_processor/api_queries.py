from base import app, api, ma, r, Resource, Flask, request
import time
import threading
import json
import hashlib

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
        message = subcription.get_message()
        print("Mensaje entrante: {}".format(message))
        if message:
            #json_object = json.loads(message)
            requests += 1
            hash = hashlib.sha512(str(message["datos"] + key).encode("utf-8")).hexdigest()
            if hash != message["hash"]:
                errors += 1
        time.sleep(3)


if __name__ == '__main__':
  
    x = threading.Thread(target=thread_function, args=(0,))
    x.start()

    app.run(debug=True, host='0.0.0.0')