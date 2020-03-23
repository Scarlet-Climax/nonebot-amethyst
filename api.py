from flask import Flask, request
import VisualGensokyo.Modified
import reversi.ruler

app = Flask(__name__)


@app.route('/chewan', methods=["GET", "POST"])
def chewan():
    return VisualGensokyo.Modified.xswl(request.form["picname"], request.form["link"])

@app.route('/reversi',methods=["GET","POST"])
def reve():
    return reversi.ruler.reversiResponse(request.form["request"])

if __name__ == '__main__':
    app.run(port=8108)
