from flask import Flask, jsonify, request
import redis
import logging
from models import db
from controller import APIController
from rabbitmq import RabbitMQ

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# set the connection details of redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 5
cache = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
logging.info(f"Using redis database db{redis_db} running at {redis_host}:{redis_port} as cache")

queue = RabbitMQ('localhost', 5672, '/', 'wb_queue')

# Initialize database within application context
with app.app_context():
    db.create_all()
    logging.info("main: Database initialized")

ctrlr = APIController(db, cache, queue, logging)

@app.route('/read-through/item/<name>', methods=['GET'])
def get_item_rt(name):
    body, status = ctrlr.read_through_get_item(name)
    return jsonify(body), status

@app.route('/cache-aside/item/<name>', methods=['GET'])
def get_item_ca(name):
    body, status = ctrlr.cache_aside_get_item(name)
    return jsonify(body), status

@app.route('/write-through/item', methods=['POST'])
def add_item_wt():
    data = request.json
    body, status = ctrlr.add_item_wt(data)
    return jsonify(body), status

@app.route('/write-around/item', methods=['POST'])
def add_item_wa():
    data = request.json
    body, status = ctrlr.add_item_wa(data)
    return jsonify(body), status

@app.route('/write-back/item', methods=['POST'])
def add_item_wb():
    data = request.json
    body, status = ctrlr.add_item_wb(data)
    return jsonify(body), status


if __name__ == '__main__':
    app.run(debug=True)
