from flask import  Flask
import hashlib

from flask import request

app=Flask(__name__)

token = "python7"

@app.route('/wechat8001')
def index():
    signature = request.args.get("signature")
    timestamp=request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr=request.args.get("echostr")

    params=[token,timestamp,nonce]
    params.sort()

    params_str= "".join(params)
    signature2=hashlib.sha1(params_str).hexdigest()

    if signature==signature2:
        return echostr
    else:
        return ""

    if __name__ == '__main__':
        app.run(debug=True)


