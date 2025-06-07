from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LICENSE_FILE = "licenses.json"

# 加载或初始化授权数据
def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "w") as f:
            json.dump({}, f)
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/check_license", methods=["POST"])
def check_license():
    data = request.json
    code = data.get("code")
    machine_id = data.get("machine_id")

    licenses = load_licenses()

    if code not in licenses:
        return jsonify({"success": False, "message": "授权码不存在"}), 400

    bound_machine = licenses[code]
    if bound_machine is None:
        licenses[code] = machine_id
        save_licenses(licenses)
        return jsonify({"success": True, "message": "授权成功并绑定"})
    elif bound_machine == machine_id:
        return jsonify({"success": True, "message": "授权通过，已绑定"})
    else:
        return jsonify({"success": False, "message": "授权码已绑定其他设备"}), 403

@app.route("/", methods=["GET"])
def hello():
    return "授权服务器已运行。POST 到 /check_license 进行授权验证。"

if __name__ == "__main__":
    app.run()
