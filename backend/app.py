import network_scanner
import port_scanner
from flask import Flask, render_template, jsonify, request
import io
import contextlib

app = Flask(__name__, template_folder='../frontend')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/api/scan-network', methods=['POST'])
def scan_network():
    data = request.get_json() or {}
    target_ip = data.get('target_ip', '').strip()
    if not target_ip:
        return jsonify({'error': 'No target_ip provided'}), 400
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            clients = network_scanner.networkscanner(target_ip)
        logs = buf.getvalue()
        return jsonify({'devices': clients, 'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan-ports', methods=['POST'])
def scan_ports():
    data = request.get_json() or {}
    target_ip = data.get('target_ip', '').strip()
    ports_range = data.get('ports_range', '').strip() or '1-65535'
    try:
        timeout = float(data.get('timeout', 1.0))
    except Exception:
        timeout = 1.0
    if not target_ip:
        return jsonify({'error': 'No target_ip provided'}), 400
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            ports = port_scanner.scanports(target_ip, ports_range=ports_range, timeout=timeout)
        logs = buf.getvalue()
        return jsonify({'ports': ports, 'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/probe-port', methods=['POST'])
def probe_port():
    data = request.get_json() or {}
    target_ip = data.get('target_ip', '').strip()
    port = data.get('port')
    if not target_ip:
        return jsonify({'error': 'No target_ip provided'}), 400
    if not port:
        return jsonify({'error': 'No port provided'}), 400
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            ports = port_scanner.scanports(target_ip, ports_range=str(int(port)), timeout=2.0, max_workers=1)
        logs = buf.getvalue()
        return jsonify({'ports': ports, 'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)