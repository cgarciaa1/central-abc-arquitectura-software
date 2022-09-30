# importing the requests library
import requests
import hashlib

# api-endpoint
URL = "http://192.168.1.145:5000/api-commands/signals"
# defining a params dict for the parameters to be sent to the API
PARAMS = {'evento' : 'Prueba'}

salt = '12345678910'

# sending get request and saving the response as response object 50 times
for a in range(50):
    value = '20° C'
    hash = hashlib.sha512(value + salt).encode("utf-8")).hexdigest()
    if a % 10 == 0
        value = '30° C'
    PARAMS = {'evento' : 'Temperatura', 'datos' : value, 'hash' : hash }
    r = requests.post(url = URL, json = PARAMS)
    print(r)

print("\nTest Auth\n")

URL_Auth = "http://192.168.1.145:5000/api-commands/authenticate"

DATA = {"username":"sensor_1", "password":"sensor1"}
DATA_BAD = {"username":"sensor_1", "password":"sensor1*"}

r = requests.get(URL_Auth)
user_info = [x for x in r.json()['monitored_users'] if x['username']=='sensor_1'][0]
assert not user_info['is_blocked'], "Usuario bloqueado"
print(user_info)

r = requests.post(URL_Auth, json=DATA)
assert r.status_code == 200, "El usuario no se puede autenticar"
print(f"{r.status_code} {r.json()}")

for i in range(3):
    r = requests.post(URL_Auth, json=DATA_BAD)
    assert r.status_code != 200, "El usuario no debería poder autenticarse"
    print(f"{r.status_code} {r.json()}")
    
    r = requests.get(URL_Auth)
    user_info = [x for x in r.json()['monitored_users'] if x['username']=='sensor_1'][0]
    assert user_info['secuential_fail_count'] == i+1, "No se suman los ingresos no exitosos"
    assert not user_info['is_blocked'], "Usuario bloqueado"
    print(user_info)

r = requests.post(URL_Auth, json=DATA_BAD)
assert r.status_code != 200, "El usuario no debería poder autenticarse"
print(f"{r.status_code} {r.json()}")

r = requests.get(URL_Auth)
user_info = [x for x in r.json()['monitored_users'] if x['username']=='sensor_1'][0]
assert user_info['is_blocked'], "El usuario debería estar bloqueado"
print(user_info)

r = requests.post(URL_Auth, json=DATA)
assert r.status_code != 200, "El usuario no debería poder autenticarse"
print(f"{r.status_code} {r.json()}")
