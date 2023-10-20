from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://test:sparta@cluster0.aum7bzn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary/get', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id' : False}))
    return jsonify({'articles': articles})

@app.route('/diary/post', methods=['POST'])
def save_diary():
   # sample_receive = request.form['sample_give']
   # print(sample_receive)

    title_receive = request.form.get('title_give'),
    content_receive = request.form.get('content_give')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f'static/{mytime}.{extension}'
    file.save(file_name)
   
    doc = {
        'file' : file_name,
        'title' : title_receive,
        'content' : content_receive,
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Data Was Saved'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)