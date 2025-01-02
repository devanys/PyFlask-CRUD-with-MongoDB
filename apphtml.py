from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import time

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB (replace with your actual MongoDB URI)
client = MongoClient(' ')
db = client[' ']  # Replace with your database name
collection = db[' ']  # Replace with your collection name

@app.route('/')
def index():
    return render_template('index.html')  # Renders the index.html template

@app.route('/data')
def get_data():
    # Retrieve the most recent data from MongoDB, sorted by timestamp
    data = []
    for record in collection.find().sort("timestamp", -1).limit(10):  # Limit to the 10 most recent entries
        data.append({
            'timestamp': record['timestamp'],
            'ir_status': record['ir_status']
        })
    
    return jsonify(data)  # Send the data as a JSON response

if __name__ == '__main__':
    app.run(debug=True)
