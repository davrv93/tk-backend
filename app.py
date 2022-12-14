from multiprocessing.util import ForkAwareLocal
from flask import Flask
import requests, base64, random, argparse, os, playsound, time, re, textwrap
from enums import voices
from flask import request
from flask_cors import CORS, cross_origin

from flask import Response


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8081"}})

@app.route('/')
def hello():
    return 'Hello, World!'



@app.route('/api/generate/', methods=['POST'])
def generate():
    try:
        print(request.form)
        data = request.form
        filename='voice.mp3'
        session_id = data.get('session_id',None)
        text_speaker = data.get('text_speaker',None)
        req_text = data.get('req_text',None)
        req_text = req_text.replace("+", "plus")
        req_text = req_text.replace(" ", "+")
        req_text = req_text.replace("&", "and")
        headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
            'Cookie': f'sessionid={session_id}'
        }
        url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
        r = requests.post(url, headers = headers)

        if r.json()["message"] == "Couldn't load speech. Try again.":
            output_data = {"status": "Session ID is invalid", "status_code": 5}
            print(output_data)
            return output_data 
        
        vstr = [r.json()["data"]["v_str"]][0]
        msg = [r.json()["message"]][0]
        scode = [r.json()["status_code"]][0]
        log = [r.json()["extra"]["log_id"]][0]
        
        dur = [r.json()["data"]["duration"]][0]
        spkr = [r.json()["data"]["speaker"]][0]

        b64d = base64.b64decode(vstr)
        
        with open(filename, "wb") as out:
            out.write(b64d)

        output_data = {
            "status": msg.capitalize(),
            "status_code": scode,
            "duration": dur,
            "speaker": spkr,
            'b64d':str(vstr),
            "log": log
        }
        #print(output_data)
        return output_data
        #return Response(output_data, status=201, mimetype='application/json')


    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Next entry.")
        print()
    

@app.after_request
def add_headers(response):
    #response.headers['Content-Type']='multipart/form-data'
    #response.headers['Content-Type']='application/json'
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='http://localhost:8081'
    response.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"


    return response
