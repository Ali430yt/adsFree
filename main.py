from flask import Flask,redirect,request,render_template,url_for,jsonify,session
import sqlite3,time,random,os,requests,json
from typing import List, Tuple, Any

namedb = "db.db"
SECRET_KEY = "6Lc1VvUqAAAAACryZkeqeZTlMZKX2PlVsJcviNX4"
PUBLIC_KEY = "6Lc1VvUqAAAAAPsDTMWXYLqnfGYOQAUp0rhpRc-x"

class DatabaseManager:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA journal_mode=WAL;')

    def create_table(self, table_name: str, columns: List[Tuple[str, str]]):
        columns_with_types = ', '.join([f"{col} {dtype}" for col, dtype in columns])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")
        self.connection.commit()

    def insert_data(self, table_name: str, data: Tuple[Any, ...]):
        placeholders = ', '.join(['?' for _ in data])
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        if table_name == "dataorders":
            last_id = self.cursor.lastrowid
        else:
            last_id = None
        self.connection.commit()
        return last_id

    def fetch_data(self, table_name: str, columns: List[str] = ["*"], condition: str = None) -> List[Tuple[Any]]:
        columns_formatted = ', '.join(columns)
        query = f"SELECT {columns_formatted} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table_name: str, updates: str, condition: str):
        query = f"UPDATE {table_name} SET {updates} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()

    def value_exists(self, table_name: str, condition: str) -> bool:
        query = f"SELECT 1 FROM {table_name} WHERE {condition} LIMIT 1"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None
    
    def delet_value(self, table_name: str, condition: str,iss=True):
        if iss == True:
            query = f"DELETE FROM {table_name} WHERE {condition}"
        else:
            query = f"DELETE FROM {table_name}"
        self.cursor.execute(query)
        self.connection.commit()

    def execute(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def close(self):
        self.connection.close()


app = Flask(__name__)
app.secret_key = "0djs9-dsd9dds-0vdcds-wecsx-cscf"

time_difference = 360

tokens = {}

def getTokenPage(page):
    tk = ''.join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnm") for i in range(random.randint(100,200)))
    current_timestamp = int(time.time())
    tokens.update({tk:{"token":tk,"page":int(page),"time":int(time.time())}})
    return tk

def checkTokenPage(tk,pg):
    if tk in tokens:
        if int(tokens[tk]["page"]) == int(pg) and (int(tokens[tk]["time"]) + time_difference) > int(time.time()):
            tokens.pop(tk)
            return True
        else:
            tokens.pop(tk)
            return False

def GetAds(ads):
    return open(ads,encoding="utf-8").read()
listcode = []

@app.route("/bot1/coin")
@app.route("/")
def index():
    if request.args.get("id"):
        session["id"] = str(request.args.get("id"))
    tk = getTokenPage(1)
    session["token"] = tk
    return render_template("index.html",token=tk,h=GetAds("h.txt"),b=GetAds("b.txt"),e=GetAds("e.txt"),rc=PUBLIC_KEY)
@app.route("/bot1/getKey")
@app.route("/getKey")
def getKey():
    captcha_response = request.args.get("g-recaptcha-response")
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret":SECRET_KEY , "response": captcha_response}
    response = requests.post(verify_url, data=payload).json()
    if response.get("success") == False:
        return redirect(url_for("index"))
    tk = request.args.get("token")
    if checkTokenPage(tk,1) and session["token"] == tk:
        tk = getTokenPage(2)
        session["token"] = tk
        return render_template("getKey.html",token=tk,h=GetAds("h.txt"),b=GetAds("b.txt"),e=GetAds("e.txt"))
    return redirect(url_for("index"))

@app.route("/bot1/show",methods=["POST","GET"])
@app.route("/show",methods=["POST","GET"])
def show():
    if request.method == "POST":
        captcha_response = request.form.get("g-recaptcha-response")
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret":SECRET_KEY , "response": captcha_response}
        response = requests.post(verify_url, data=payload).json()
        t3 = request.form.get("tid")
        if response.get("success") and checkTokenPage(t3,3) and session["token"] == t3:
            id = "".join(random.choices('1234567890',k=50))
            listcode.append({
                "id":id,
                "type":"addCoin",
                "user_id":session["id"]
            })
            print(listcode)
        else:
            return redirect(url_for("index"))
    tk = request.args.get("token")
    if checkTokenPage(tk,2) and session["token"] == tk:
        tk = getTokenPage(3)
        session["token"] = tk
        return render_template("show.html",t3=tk,rc=PUBLIC_KEY,h=GetAds("h.txt"),b=GetAds("b.txt"),e=GetAds("e.txt"))
    return redirect(url_for("index"))


@app.route("/bot1/api/get/user/code/list")
def apiList():
    return jsonify(listcode)


@app.route("/bot1/api/delet/user/code/list/<id>")
def apiListDelet(id):
    for i in listcode:
        if str(i['id']) == id:
            listcode.remove(id)
    return jsonify(listcode)



@app.route("/bot2/coin")
def index2():
    if request.args.get("id"):
        session["id"] = str(request.args.get("id"))
    tk = getTokenPage(1)
    session["token"] = tk
    return render_template("index.html",token=tk,h=GetAds("h2.txt"),b=GetAds("b2.txt"),e=GetAds("e2.txt"),rc=PUBLIC_KEY)

@app.route("/bot2/getKey")
def getKey2():
    captcha_response = request.args.get("g-recaptcha-response")
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret":SECRET_KEY , "response": captcha_response}
    response = requests.post(verify_url, data=payload).json()
    if response.get("success") == False:
        return redirect(url_for("index"))
    tk = request.args.get("token")
    if checkTokenPage(tk,1) and session["token"] == tk:
        tk = getTokenPage(2)
        session["token"] = tk
        return render_template("getKey.html",token=tk,h=GetAds("h2.txt"),b=GetAds("b2.txt"),e=GetAds("e2.txt"))
    return redirect(url_for("index"))

@app.route("/bot2/show",methods=["POST","GET"])
def show2():
    if request.method == "POST":
        captcha_response = request.form.get("g-recaptcha-response")
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret":SECRET_KEY , "response": captcha_response}
        response = requests.post(verify_url, data=payload).json()
        t3 = request.form.get("tid")
        if response.get("success") and checkTokenPage(t3,3) and session["token"] == t3:
            id = "".join(random.choices('1234567890',k=50))
            listcode.append({
                "id":id,
                "type":"addCoin",
                "user_id":session["id"]
            })
            print(listcode)
        else:
            return redirect(url_for("index"))
    tk = request.args.get("token")
    if checkTokenPage(tk,2) and session["token"] == tk:
        tk = getTokenPage(3)
        session["token"] = tk
        return render_template("show.html",t3=tk,rc=PUBLIC_KEY,h=GetAds("h2.txt"),b=GetAds("b2.txt"),e=GetAds("e2.txt"))
    return redirect(url_for("index"))

@app.route("/sw.js")
def swhs():
    return GetAds("sw.js")

@app.route("/bot2/api/get/user/code/list")
def apiList2():
    return jsonify(listcode)


@app.route("/bot2/api/delet/user/code/list/<id>")
def apiListDelet2(id):
    for i in listcode:
        if str(i['id']) == id:
            listcode.remove(id)
    return jsonify(listcode)
if __name__ == "__main__":
    app.run(host="0.0.0.0")