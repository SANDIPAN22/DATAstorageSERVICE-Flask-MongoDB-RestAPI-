from flask import Flask,request,jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import bcrypt as bc
app=Flask(__name__)
api=Api(app)

client=MongoClient("localhost",27017)
db=client["apiServiceDB"]
col=db["apiServiceTB"]

def varify(user1,pass1):
    #if(col.find({"username":user1}).count()==1):
        x=col.find({"username":user1})[0]
        if bc.checkpw(pass1.encode('utf-8'), x["password"]):
            tok=x["token"]
            if(tok>0):
                return tok,200
            else:
                return tok,302
        else:
            return 0,301

class Registration(Resource):
    def post(self):

        data=request.get_json()
        username=data["user"]
        password=data["psw"]
        #return str(type((username)))
        passb = bytes(password, 'utf-8')
        hashedpw=bc.hashpw(password.encode('utf-8') ,bc.gensalt())
        col.insert(
        {
        "username":username,
        "password":hashedpw,
        "token":10,
        "sentence":[],
        }
        )
        ret={
        "message":"SUCCESSFULLY REGISTERED !! ",
        "Token":10,
        "Status Code":200
        }
        return jsonify(ret)

class Insert(Resource):
    def post(self):
        data=request.get_json()
        user1=data["user"]
        pass1=data["psw"]
        sen1=data["sen"]

        n_toc,scode=varify(user1,pass1)
        if(scode==200):
            col.update({"username":user1},{
            "$set":{"token":n_toc-1},
            "$push":{"sentence":sen1}

            })
            ret={
            "Message":"SUCCESSFULLY INSERTED !",
            "Token":n_toc-1,
            "Status Code":scode

            }
            return jsonify(ret)
        elif(scode==301):
            ret={
            "Message":"wrong password or username",

            "Status Code":scode
            }
            return jsonify(ret)
        else:
            ret={
            "Message":"NOT ENOUGH TOKEN TO PERFORM THIS ACTION  ! BUY NOW!!",

            "Status Code":scode

            }
            return jsonify(ret)

class Read(Resource):
    def post(self):
        data=request.get_json()
        user1=data["user"]
        pass1=data["psw"]


        n_toc,scode=varify(user1,pass1)
        if(scode==200):
            s=col.find({"username":user1})[0]["sentence"]
            col.update({"username":user1},{
            "$set":{"token":n_toc-1}})

            ret={
            "Message":s,
            "Token":n_toc-1,
            "Status Code":scode

            }
            return jsonify(ret)
        elif(scode==301):
            ret={
            "Message":"wrong password or username",

            "Status Code":scode
            }
            return jsonify(ret)
        else:
            ret={
            "Message":"NOT ENOUGH TOKEN TO PERFORM THIS ACTION  ! BUY NOW!!",

            "Status Code":scode

            }
            return jsonify(ret)




api.add_resource (Registration,'/regis')
api.add_resource (Insert,'/insert')
api.add_resource (Read,'/read')
if __name__=="__main__":
    app.run(debug=True)
