from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

LICENSE_FILE = "licenses.json"

def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        return {}
    try:
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/check_license", methods=["POST"])
def check_license():
    try:
        data = request.get_json()
        license_code = data.get("license_code", "").strip()
        machine_id = data.get("machine_id", "").strip()

        if not license_code or not machine_id:
            return jsonify({"status": "error", "message": "Missing license_code or machine_id"}), 400

        licenses = load_licenses()

        if license_code not in licenses:
            # ✅ 首次激活：授权码未被使用，绑定机器码
            licenses[license_code] = machine_id
            save_licenses(licenses)
            return jsonify({"status": "ok", "message": "License activated"})

        if licenses[license_code] == machine_id:
            # ✅ 授权码绑定的机器码匹配
            return jsonify({"status": "ok", "message": "License valid"})

        # ❌ 授权码存在但绑定了其他机器码
        return jsonify({"status": "error", "message": "License already used on another machine"}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": f"Internal server error: {e}"}), 500

@app.route("/")
def index():
    return "✅ License server running"
