from flask import Flask, render_template, request
import os, pickle

app = Flask(__name__)

BASE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "model_fps_predictor.pkl")

bundle = {"encoders": {"cpus": [], "gpus": [], "ram_gb": [], "games": [],
                       "resolutions": ["1280x720","1600x900","1920x1080","2560x1440"],
                       "quality": ["Low","Medium","High","Ultra"]}}
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        bundle = pickle.load(f)
        model = bundle.get("model")
enc = bundle["encoders"]

@app.route("/", methods=["GET","POST"])
def index():
    result = None
    cpus = enc.get("cpus") or ["Snapdragon 720G","Snapdragon 870","Snapdragon 8 Gen 1","Snapdragon 8 Gen 2"]
    gpus = enc.get("gpus") or ["Adreno 618","Adreno 650","Adreno 730"]
    rams = enc.get("ram_gb") or [4,6,8,12,16]
    games = enc.get("games") or ["BGMI / PUBG Mobile","Call of Duty: Mobile","Genshin Impact","Free Fire MAX","Asphalt 9"]
    resolutions = enc.get("resolutions") or ["1280x720","1600x900","1920x1080"]
    quality = enc.get("quality") or ["Low","Medium","High"]

    if request.method == "POST":
        cpu = request.form.get("cpu", cpus[0])
        gpu = request.form.get("gpu", gpus[0])
        ram = int(request.form.get("ram", 6))
        game = request.form.get("game", games[0])
        target = int(request.form.get("target_fps", 60))

        res = "1920x1080" if ram >= 8 else "1280x720"
        q = "High" if ram >= 12 else ("Medium" if ram >= 6 else "Low")
        est = 60 if q=="High" else (50 if q=="Medium" else 40)
        result = {"cpu":cpu,"gpu":gpu,"ram":ram,"game":game,"target":target,
                  "resolution":res,"quality":q,"estimated_fps":est,
                  "toggles":{"VSync":"Off","Motion Blur":"Off"}}

    return render_template("index.html",enc={"cpus":cpus,"gpus":gpus,"ram_gb":rams,
                                             "games":games,"resolutions":resolutions,"quality":quality},
                           result=result)
