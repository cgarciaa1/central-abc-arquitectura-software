# importing the requests library
import requests

# api-endpoint
URL = "http://192.168.1.145:5000/api-commands/signals"
# defining a params dict for the parameters to be sent to the API
PARAMS = {'evento' : 'Prueba'}

# sending get request and saving the response as response object 50 times
for a in range(50):
    r = requests.post(url = URL, json = PARAMS)
    print(r)