from flask import Flask, jsonify, request
import os
import time
import random

app = Flask(__name__)  #trying to set up my flaskapp

MODE = os.environ.get("MODE", "stable")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
start_time = time.time()
chaos_mode = None
chaos_value = None

@app.route("/")
def welcome():
     return jsonify({
        "message": f"You're welcome! Running in {MODE} mode",
        "version": f"{APP_VERSION}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })

@app.route("/healthz")
def check_status():
     return jsonify({
          "status": "Healthy",
          "uptime": round(time.time() - start_time, 2)
     })
     
@app.after_request
def mode(response):
     if MODE == "canary":
      response.headers["X-Mode"] = "Canary"
     return response

@app.before_request
def duration():
    global chaos_mode, chaos_value
    if chaos_mode == "slow":
        time.sleep(chaos_value)
    elif chaos_mode == "error":
        if random.random() < chaos_value:
            return jsonify({"error": "Internal server error"}), 500


@app.route("/chaos", methods=["POST"])
def chaos():
    if MODE != "canary":
        return "Error. Not in canary mode"
    data = request.get_json()

    global chaos_mode, chaos_value

    if data["mode"] == "slow":
        chaos_mode = "slow"
        chaos_value = data["duration"] 
        return jsonify({
           "status": "chaos activated",
           "chaos_mode": chaos_mode,
           "chaos_value": chaos_value
       })
    
    elif data["mode"] == "error":
        chaos_mode = "error"
        chaos_value = data["rate"]
        return jsonify({
           "status": "chaos activated",
           "chaos_mode": chaos_mode,
           "chaos_value": chaos_value
       })

    elif data["mode"] == "recover":
       chaos_mode = None
       chaos_value = None
       return jsonify({
           "status": "chaos deactivated",
           "chaos_mode": None,
           "chaos_value": None
       }) 

       
       




if __name__ == "__main__":
    app.run(port=8888, debug=True)
