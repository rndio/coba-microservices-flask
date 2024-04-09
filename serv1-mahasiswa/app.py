from flask import Flask , request, jsonify
import pymysql
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError, validates

# Inisialisasi Flask & Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)

# Schema untuk validasi data mahasiswa
class MahasiswaSchema(ma.Schema):
  nim = fields.String(required=True,validate=[fields.Length(min=10, max=10, error='NIM harus 10 digit')])
  nama = fields.String(required=True, validate=[fields.Length(min=3, max=60, error='Nama harus 3-60 karakter')])
  jk = fields.String(required=True)
  prodi = fields.String(required=True, validate=[fields.Length(min=3, max=60, error='Prodi harus 3-60 karakter')])

  @validates('nim')
  def validate_nim(self, value):
    # Cek apakah NIM berupa angka
    if not value.isdigit():
      raise ValidationError('NIM harus berupa angka')
    # Cek apakah NIM sudah terdaftar
    cursor = db.cursor()
    cursor.execute("SELECT nim FROM mahasiswa WHERE nim = %s", (value))
    result = cursor.fetchone()
    cursor.close()
    if result is not None:
      raise ValidationError('NIM sudah terdaftar')

  @validates('jk')
  def validate_jk(self, value):
    if value not in ['L', 'P']:
      raise ValidationError('Jenis Kelamin harus L atau P')

# Koneksi.py :D
db = pymysql.connect(
  host = 'localhost',
  user = 'root',
  password = '',
  db = 'db_mahasiswa',
  cursorclass=pymysql.cursors.DictCursor
)

# Route /
@app.route("/")
def hello_world():
    return 'Kelompok 6: Server 1 (Mahasiswa)'

# Route untuk menampilkan data semua mahasiswa
@app.route("/mahasiswa", methods=['GET'])
def mahasiswa_index():
  cursor = db.cursor()
  cursor.execute("SELECT nim,nama,jk,prodi FROM mahasiswa")
  result = cursor.fetchall()
  cursor.close()
  return jsonify({"status": 'success',"data": result})

# Route untuk menampilkan data mahasiswa berdasarkan NIM
@app.route("/mahasiswa/<nim>", methods=['GET'])
def mahasiswa_show(nim):

  if not nim.isdigit():
    return jsonify({"status": 'error',"message": 'NIM harus berupa angka'}), 400
  elif len(nim) != 10:
    return jsonify({"status": 'error',"message": 'NIM harus 10 digit'}), 400

  cursor = db.cursor()
  cursor.execute("SELECT nim,nama,jk,prodi FROM mahasiswa WHERE nim = %s", (nim))
  result = cursor.fetchone()
  cursor.close()

  if result is None:
    return jsonify({"status": 'error',"message": 'Data mahasiswa tidak ditemukan'}), 404

  return jsonify({
    "status": 'success',
    "data": result
  })

# Route untuk menyimpan data mahasiswa
@app.route("/mahasiswa", methods=['POST'])
def mahasiswa_store():
  mahasiswa_schema = MahasiswaSchema()

  try:
    data = mahasiswa_schema.load(request.json)
    cursor = db.cursor()
    cursor.execute("INSERT INTO mahasiswa (nim, nama, jk, prodi) VALUES (%s, %s, %s, %s)", (
      data['nim'],
      data['nama'],
      data['jk'],
      data['prodi']
    ))
    db.commit()
    cursor.close()
    return jsonify({"status": 'success',"message": 'Data mahasiswa berhasil disimpan'}), 201
  except ValidationError as err:
    return jsonify({"status": 'error', "message": err.messages}), 400

# Route untuk mengupdate data mahasiswa berdasarkan NIM
@app.route("/mahasiswa/<nim>", methods=['PUT'])
def mahasiswa_update(nim):
  if not nim.isdigit():
    return jsonify({"status": 'error',"message": 'NIM harus berupa angka'}), 400
  elif len(nim) != 10:
    return jsonify({"status": 'error',"message": 'NIM harus 10 digit'}), 400

  mahasiswa_schema = MahasiswaSchema(partial=True)
  try:
    data = mahasiswa_schema.load(request.json)
    updated_fields = []

    # Cek apakah data yang akan diupdate ada di request
    if 'nama' in data:
      updated_fields.append(('nama', data['nama']))
    if 'jk' in data:
      updated_fields.append(('jk', data['jk']))
    if 'prodi' in data:
      updated_fields.append(('prodi', data['prodi']))

    if not updated_fields:
      return jsonify({"status": 'error',"message": 'Tidak ada perubahan data'}), 400

    cursor = db.cursor()

    # Construct the SQL UPDATE query with prepared statement
    query = "UPDATE mahasiswa SET "
    query += ", ".join(f"{field} = %s" for field, _ in updated_fields)
    query += " WHERE nim = %s"

    # Append nim to the list of values for the WHERE clause
    values = [value for _, value in updated_fields]
    values.append(nim)

    # Execute the prepared statement with parameters
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({"status": 'success',"message": 'Data mahasiswa berhasil diupdate'})
  except ValidationError as err:
    return jsonify({"status": 'error', "message": err.messages}), 400


# Route untuk menghapus data mahasiswa berdasarkan NIM
@app.route("/mahasiswa/<nim>", methods=['DELETE'])
def mahasiswa_delete(nim):
  if not nim.isdigit():
    return jsonify({"status": 'error',"message": 'NIM harus berupa angka'}), 400
  elif len(nim) != 10:
    return jsonify({"status": 'error',"message": 'NIM harus 10 digit'}), 400
  cursor = db.cursor()
  cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim))
  db.commit()
  cursor.close()

  if cursor.rowcount == 0:
    return jsonify({"status": 'error',"message": 'Data mahasiswa tidak ditemukan'}), 404

  return jsonify({
    "status": 'success',
    "message": 'Data mahasiswa berhasil dihapus'
  })


if __name__ == '__main__':
    app.run(port = 5000, debug=True)