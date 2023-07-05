import os

import requests
from flask import Flask, jsonify, make_response, request
from flask_restful import Api

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route('/api/stats', methods=['GET'])
def getJwt():
    story_url = request.args.get('story_url')
    if not "http" in story_url:
        return make_response(jsonify(msg="Not authorized"), 403)
    else:
        c = requests.get(story_url).content.decode("utf-8")

        try:        
            a = c.split("clapCount\":")[1]
            endIndex = a.index(",")
            claps = int(a[0:endIndex])
        except Exception:
            claps = 0  

        try:   
            b = c.split("voterCount\":")[1]
            endIndex = b.index(",")
            voterCount = int(b[0:endIndex])
        except Exception:
            voterCount = 0          
        
        try:
            d = c.split("\"PostResponses\",\"count\":")[1]
            endIndex = d.index("}")
            comments = int(d[0:endIndex])
        except Exception:
            comments = 0           

        return jsonify(claps=claps, voterCount=voterCount, comments=comments)


api = Api(app)
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)