from flask import Flask, request
import logging
import uuid
from pythonjsonlogger import jsonlogger
import requests

app = Flask(__name__)

log = logging.getLogger("service1_logger")
logHandler = logging.FileHandler('/app/logs/service1.log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s request_id=%(request_id)s, source=%(source)s, destination=%(destination)s')
logHandler.setFormatter(formatter)
log.addHandler(logHandler)
log.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request.request_id = request_id
    log.info("Received request", extra={'request_id': request_id})

@app.route('/')
def index():
    return "Hello from Service 1!"

@app.route('/forward')
def forward():
    request_id = request.request_id
    headers = {
        'X-Request-ID': request_id,
        'X-Source-ID': request.url 
    }
    
    log.info("Forwarding request", extra={
        'request_id': request_id,
        'source': request.url,
        'destination': 'http://service2:5002/'
    })
    
    response = requests.get('http://service2:5002/', headers=headers)
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
