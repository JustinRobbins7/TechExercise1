from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from datetime import datetime
from time import strptime

app = Flask(__name__)
mysql = MySQL()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MYSQL_DATABASE_USER'] = 'dev'
app.config['MYSQL_DATABASE_PASSWORD'] = 'TechEx1'
app.config['MYSQL_DATABASE_DB'] = 'FlaskTechApp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return ReloadData()

@app.route("/",methods=['POST'])
def handleInput():        
    print('Entering Event!')        
    _event_name = request.form['inputEvent']
    _event_loc = request.form['inputLoc']
    _event_desc = request.form['inputDesc']
    _html_date_input = request.form['inputDateTime']
     
    _html_date = datetime(*(strptime(_html_date_input, "%Y-%m-%dT%H:%M")[0:6]))
    _event_date = datetime.strftime(_html_date, "%Y-%m-%d %H:%M:%S")
    
    if _event_name and _event_loc and _event_desc and _html_date_input:
        return EnterIntoDB((_event_name, _event_loc, _event_date, _event_desc))
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/handledeletion', methods=['POST'])
def handledeletion():
    print('PING!')
    TruncateData()
    return ReloadData()

def EnterIntoDB(argtuple):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('create_event',argtuple)
    data = cursor.fetchall()
    
    if len(data) is 0:
        conn.commit()
        conn.close()
        return json.dumps({'message':'entry successful!'})
    else:
        conn.close()
        return json.dumps({'error':str(data[0])})

def ReloadData():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return render_template('index.html', events = events)  

def TruncateData():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('TRUNCATE TABLE events')
    events = cursor.fetchall()
    conn.commit()
    conn.close()
    return;

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
    TruncateData()
