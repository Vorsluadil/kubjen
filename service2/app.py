from flask import Flask, request
import logging
import uuid
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

log = logging.getLogger("service2_logger")
logHandler = logging.FileHandler('/app/logs/service2.log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s request_id=%(request_id)s, source=%(source)s, destination=%(destination)s')
logHandler.setFormatter(formatter)
log.addHandler(logHandler)
log.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request.request_id = request_id

    source = request.headers.get('X-Source-ID', 'unknown source')

    log.info("Received request", extra={
        'request_id': request_id,
        'source': source, 
    })

@app.route('/')
def home():
    return "Hello from Service 2!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
