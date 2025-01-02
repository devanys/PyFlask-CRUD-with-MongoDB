import serial
import time
from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi ke MongoDB Atlas
client = MongoClient('mongodb+srv://devan:devanyusfa@cluster0.eobvtld.mongodb.net/')
db = client['ZZ']
collection = db['UU']

# Koneksi ke Arduino
ser = serial.Serial('COM4', 9600)
time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    data = []
    for record in collection.find().sort("timestamp", -1):  # Sort by timestamp descending
        data.append({
            'timestamp': record['timestamp'],
            'ir_status': record['ir_status']  # Update to reflect the proximity sensor status
        })
    print(f"Data retrieved from MongoDB: {data}")  # Log data to the console
    return jsonify(data)

def read_ir_sensor():
    while True:
        try:
            # Baca data dari serial dan decode
            ir_status = ser.readline().decode().strip()  # Read and clean up the IR sensor data
            
            if ir_status.isdigit():  # Make sure it's a valid digit (0 or 1)
                ir_status = int(ir_status)
                
                # Membuat data untuk disimpan di MongoDB
                record = {
                    'ir_status': ir_status,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                collection.insert_one(record)
                print(f"Data inserted: {record}")
                
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

if __name__ == '__main__':
    # Start the IR sensor reading in a background thread
    from threading import Thread
    sensor_thread = Thread(target=read_ir_sensor)
    sensor_thread.daemon = True
    sensor_thread.start()
    
    app.run(debug=True)
