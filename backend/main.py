import network_scanner
import port_scanner
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "net-dashboard running"
