from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

# IP dari mikroservis yang akan diakses
IP_SERVER1 = 'http://110.239.67.185:2001/'
IP_SERVER2 = 'http://110.239.71.252:2002/'

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'RAHASIA_BANGET_'

jwt = JWTManager(app)

users = [
  {
    "id": 1,
    "name": "Administrator",
    "username": "admin",
    "password": "admin"
  }
]

# Fungsi untuk meneruskan permintaan ke mikroservis tertentu
def forward_request(service_url, endpoint, method='GET', data=None):
    url = f"{service_url}/{endpoint}"
    if method == 'GET':
        response = requests.get(url, params=data)
    elif method == 'POST':
        response = requests.post(url, json=data)
    elif method == 'PUT':
        response = requests.put(url, json=data)
    elif method == 'DELETE':
        response = requests.delete(url)
    return response.json(), response.status_code

@app.route("/")
def hello_world():
    return "Kelompok 6: Server 0 Gateway"

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = [user for user in users if user['username'] == username and user['password'] == password]
    if user:
        access_token = create_access_token({
            'id': user[0]['id'],
            'username': user[0]['username'],
            'name': user[0]['name']
        })
        return jsonify(access_token=access_token)
    return jsonify(message="Invalid username or password"), 401

@app.route("/protected", methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Route untuk menampilkan data semua mahasiswa
@app.route("/mahasiswa", methods=['GET'])
@jwt_required()
def mahasiswa_index():
    service_url = IP_SERVER1
    endpoint = 'mahasiswa'
    data = request.args.to_dict()
    response_data, status_code = forward_request(service_url, endpoint, method='GET', data=data)
    return jsonify(response_data), status_code

# Route untuk menampilkan data mahasiswa berdasarkan NIM
@app.route("/mahasiswa/<nim>", methods=['GET'])
@jwt_required()
def mahasiswa_show(nim):
    service_url = IP_SERVER1
    endpoint = f"mahasiswa/{nim}"
    response_data, status_code = forward_request(service_url, endpoint, method='GET')
    return jsonify(response_data), status_code

# Route untuk menyimpan data mahasiswa
@app.route("/mahasiswa", methods=['POST'])
@jwt_required()
def mahasiswa_store():
    service_url = IP_SERVER1
    endpoint = 'mahasiswa'
    data = request.json
    response_data, status_code = forward_request(service_url, endpoint, method='POST', data=data)
    return jsonify(response_data), status_code

# Route untuk mengupdate data mahasiswa berdasarkan NIM
@app.route("/mahasiswa/<nim>", methods=['PUT'])
@jwt_required()
def mahasiswa_update(nim):
    service_url = IP_SERVER1
    endpoint = f"mahasiswa/{nim}"
    data = request.json
    response_data, status_code = forward_request(service_url, endpoint, method='PUT', data=data)
    return jsonify(response_data), status_code

# Route untuk menghapus data mahasiswa berdasarkan NIM
@app.route("/mahasiswa/<nim>", methods=['DELETE'])
@jwt_required()
def mahasiswa_delete(nim):
    service_url = IP_SERVER1
    endpoint = f"mahasiswa/{nim}"
    response_data, status_code = forward_request(service_url, endpoint, method='DELETE')
    return jsonify(response_data), status_code

# Route untuk mendapatkan data provinsi
@app.route("/ongkir/province/", methods=['GET'])
@jwt_required()
def province_get():
    service_url = IP_SERVER2
    endpoint = 'ongkir/province'
    data = request.args.to_dict()
    response_data, status_code = forward_request(service_url, endpoint, method='GET', data=data)
    return jsonify(response_data), status_code

# Route untuk mendapatkan data kota
@app.route("/ongkir/city/", methods=['GET'])
@jwt_required()
def cities_get():
    service_url = IP_SERVER2
    endpoint = 'ongkir/city'
    data = request.args.to_dict()
    response_data, status_code = forward_request(service_url, endpoint, method='GET', data=data)
    return jsonify(response_data), status_code

# Route untuk mendapatkan data biaya pengiriman
@app.route("/ongkir/cost/", methods=['GET'])
@jwt_required()
def cost_get():
    service_url = IP_SERVER2
    endpoint = 'ongkir/cost'
    data = request.args.to_dict()
    response_data, status_code = forward_request(service_url, endpoint, method='GET', data=data)
    return jsonify(response_data), status_code

if __name__ == "__main__":
    app.run('0.0.0.0', port=2000, debug=True)