from flask import Flask,request,redirect,render_template,url_for,jsonify
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://Imran_riaz_chohan:Audionic123@cluster0-k8jot.mongodb.net/todolistapp'

mongo = PyMongo(app)

@app.route('/',methods=['GET'])
def hello():
    return jsonify({"message":"it's working"})

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_all_frameworks():
    framework = mongo.db.test 

    output = []

    for q in framework.find():
        output.append({'_id' : q['_id'], 'title' : q['title'],'describtion':q['describtion'],'done':q['done']})

    return jsonify({'result' : output})

@app.route('/todo/api/v1.0/tasks/<int:name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.test

    q = framework.find_one({'_id' : name})
    # output = {'_id' : q['_id'], 'title' : q['title'],'describtion':q['describtion'],'done':q['done']}
    if q:
        output = {'_id' : q['_id'], 'title' : q['title'],'describtion':q['describtion'],'done':q['done']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def add_framework():
    framework = mongo.db.test

    id = request.json['_id']
    title = request.json['title']
    describtion= request.json['describtion']
    done=request.json['done']

    framework_id = framework.insert({'_id' : id, 'title' : title,'describtion':describtion,'done':done})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'_id' : new_framework['_id'], 'title' : new_framework['title'],'describtion':new_framework['describtion'],'done':new_framework['done']}

    return jsonify({'result' : output})

@app.route('/todo/api/v1.0/tasks/<int:name>', methods=['PUT'])
def edit_one_framework(name):
    framework = mongo.db.test
    q = framework.find_one({'_id' : name})
    id = request.json['_id']
    title = request.json['title']
    describtion= request.json['describtion']
    done=request.json['done']

    
    newvalues = { "$set": { '_id' : id,'title' : title ,'describtion' : describtion,'done':done} }

    framework.update_many(q, newvalues)


    output = {'_id' : q['_id'], 'title' : q['title'],'describtion':q['describtion'],'done':q['done']}

    return jsonify({'result' : output})

@app.route('/todo/api/v1.0/tasks/<int:name>', methods=['DELETE'])
def delete_one_framework(name):
    framework = mongo.db.test
    q = framework.find_one({'_id' : name})
    if q :
        framework.remove(q,True)
    else:
        q="NOt found"
    return jsonify({"result ": q})    
if __name__ == "__main__":
    app.run(debug=True,port=5000)