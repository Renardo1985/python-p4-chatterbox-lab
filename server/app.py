from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods =['GET','POST'])
def messages():
        
    if request.method == 'GET':
        messages = []
        for msg in Message.query.all():    
            msg_dic = msg.to_dict()        
            messages.append(msg_dic)
    
        response = make_response(jsonify(messages),200)
        response.headers["Content-Type"] = "application/json"    
        return response
    
    elif request.method == 'POST':
        
        data = request.get_json()
        new_msg = Message(body = data.get("body"),username = data.get("username"))
        db.session.add(new_msg)
        db.session.commit()
        
        msg_dict = new_msg.to_dict()
        response = make_response(jsonify(msg_dict),201)        
        return response

@app.route('/messages/<int:id>',methods =['PATCH','DELETE'])
def messages_by_id(id):
    
    if request.method == 'PATCH':
        data = request.get_json()
        new_body = data.get('body')
        
        message = db.session.query(Message).filter_by(id=id).first()
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        message.body = new_body
        db.session.commit()
        
        msg_dict = message.to_dict()
        response = make_response(jsonify(msg_dict),201)        
        return response
    
    if request.method == 'DELETE':
        message = db.session.query(Message).filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted'}), 204 

        

if __name__ == '__main__':
    app.run(port=5555)
