from flask import Flask, render_template, request, json
import datetime, time

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/",methods=['POST'])
def enterEvent():
    _event_name = request.form['inputEvent']
    _event_loc = request.form['inputLoc']
    _event_desc = request.form['inputDesc']
    _html_date_input = request.form['inputDateTime']
    """ 
    _html_date = strptime(_html_date_input, "%b. %d, %Y, %I %p")
    _event_date = strftime(_html_date, "%Y-%m-%d %H:%M:%S")
    """

    if _event_name and _event_loc and _event_desc and _html_date_input:
        return json.dumps({'html':'<span>'+ _html_date_input +'</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
