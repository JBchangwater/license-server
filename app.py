from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LICENSE_FILE = "licenses.json"

def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, 'r') as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route("/check_license", methods=["POST"])
def check_license():
    data = request.get_json()
    license_code = data.get("license_code")
    machine_id = data.get("machine_id")

    if not license_code or not machine_id:
        return jsonify({"status": "error", "message": "Missing license_code or machine_id"}), 400

    licenses = load_licenses()

    if license_code not in licenses:
        # 第一次激活，绑定机器码
        licenses[license_code] = machine_id
        save_licenses(licenses)
        return jsonify({"status": "ok", "message": "License activated"})

    if licenses[license_code] == machine_id:
        # 已授权且机器码匹配
        return jsonify({"status": "ok", "message": "License valid"})

    return jsonify({"status": "error", "message": "License already used on another machine"}), 403

@app.route("/")
def hello():
    return "License server is running."
