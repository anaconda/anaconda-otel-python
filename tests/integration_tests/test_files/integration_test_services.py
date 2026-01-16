# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import requests
import threading
import time
from flask import Flask, request, jsonify
from anaconda.opentelemetry.signals import initialize_telemetry, get_trace
from anaconda.opentelemetry import Configuration, ResourceAttributes

app_a = Flask(__name__)

@app_a.route('/')
def service_a_handler():
    carrier = {}
    with get_trace("serviceA.process", {"service": "A", "id": "123"}, carrier) as span:
        span.add_event("started")
        response = requests.post('http://localhost:8002/process', 
                                json={"carrier": carrier, "data": "hello"})
        result = response.json()
    return jsonify({"from": "A", "result": result, "carrier": carrier})


app_b = Flask(__name__)

@app_b.route('/process', methods=['POST'])
def service_b_handler():
    data = request.json
    carrier = data.get('carrier', {})
    with get_trace("serviceB.process", {"service": "B"}, carrier) as span:
        span.add_event("processing")
        response = requests.post('http://localhost:8003/process',
                                json={"carrier": carrier, "data": data['data'].upper()})
        result = response.json()
    return jsonify({"from": "B", "result": result})


app_c = Flask(__name__)

@app_c.route('/process', methods=['POST'])
def service_c_handler():
    data = request.json
    carrier = data.get('carrier', {})
    with get_trace("serviceC.process", {"service": "C"}, carrier) as span:
        span.add_event("finalizing")
    return jsonify({"from": "C", "data": data['data'], "done": True})

def start_services():

    # always init telemetry
    config = Configuration(default_endpoint='http://localhost:4318').set_console_exporter(use_console=True)
    attrs = ResourceAttributes('test_span_svc', 'v1.0.0')
    initialize_telemetry(config, attrs, signal_types=['tracing'])

    from werkzeug.serving import make_server
    
    servers = []
    threads = []
    
    server_a = make_server('localhost', 8001, app_a)
    server_b = make_server('localhost', 8002, app_b)
    server_c = make_server('localhost', 8003, app_c)
    
    servers = [server_a, server_b, server_c]
    
    for server in servers:
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    time.sleep(0.5)
    
    return servers

def stop_services(servers):
    for server in servers:
        server.shutdown()