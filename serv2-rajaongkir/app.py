from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "6549071c1ef58bf4a789d8cb30827f55"
API_URL = "https://api.rajaongkir.com/starter"

headers = {'key': API_KEY}

@app.route("/")
def hello_world():
    return "Kelompok 6: Server 2 (RajaOngkir)"

# Route untuk mendapatkan data provinsi
@app.route("/ongkir/province/", methods=['GET'])
def province_get():
    apiURL = API_URL + "/province"
    params = {}

    # Jika terdapat query parameter id
    if request.args.get('id'):
      idProvinsi = request.args.get('id')
      params['id'] = idProvinsi

    # Gabungkan query parameter di apiURL
    if params:
      apiURL = f"{apiURL}?{'&'.join([f'{key}={value}' for key,value in params.items()])}"

    response = requests.get(f"{apiURL}", headers=headers)
    return response.json()

# Route untuk mendapatkan data kota
@app.route("/ongkir/city/", methods=['GET'])
def cities_get():
    apiURL = API_URL + "/city"
    params = {}

    # Jika terdapat query parameter id
    if request.args.get('id'):
      idKota = request.args.get('id')
      params['id'] = idKota

    # Jika terdapat query parameter province
    if request.args.get('province'):
      idProvinsi = request.args.get('province')
      params['province'] = idProvinsi

    # Gabungkan query parameter di apiURL
    if params:
      apiURL = f"{apiURL}?{'&'.join([f'{key}={value}' for key,value in params.items()])}"

    response = requests.get(f"{apiURL}", headers=headers)
    return response.json()

# Route untuk mendapatkan data biaya pengiriman
@app.route("/ongkir/cost/", methods=['GET'])
def cost_get():
    apiURL = API_URL + "/cost"
    params = {}

    # Jika terdapat query parameter origin
    if request.args.get('origin'):
      origin = request.args.get('origin')
      params['origin'] = origin

    # Jika terdapat query parameter destination
    if request.args.get('destination'):
      destination = request.args.get('destination')
      params['destination'] = destination

    # Jika terdapat query parameter weight
    if request.args.get('weight'):
      weight = request.args.get('weight')
      params['weight'] = weight

    # Jika terdapat query parameter courier
    if request.args.get('courier'):
      courier = request.args.get('courier')
      params['courier'] = courier

    response = requests.post(f"{apiURL}", headers=headers, data=params)
    return response.json()

if __name__ == "__main__":
    app.run(port=5001, debug=True)