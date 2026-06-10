import os
import time
from flask import Flask, redirect, make_response

app = Flask(__name__)

CLOUDINARY_BASE_URL = "https://res.cloudinary.com/dz1g0fxmd/image/upload/edualflow/ultima.jpg"

@app.route("/")
def home():
    return "EdualFlow image service OK"

@app.route("/ultima.jpg")
def ultima_imaxe():
    url = f"{CLOUDINARY_BASE_URL}?t={int(time.time())}"
    response = make_response(redirect(url, code=302))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
