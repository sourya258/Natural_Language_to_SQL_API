from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.exc import SQLAlchemyError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:gublu%40sql9@localhost/contact_db"
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
db = SQLAlchemy(app)
limiter = Limiter(get_remote_address, app=app, default_limits=['7200 per day', '300 per hour'])

#Contact Model
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(Integer,primary_key = True, nullable = False, unique = True)
    phoneNumber = db.Column(String(20),nullable = True)
    email = db.Column(String(100),nullable = True)
    linkedid = db.Column(Integer, ForeignKey('contacts.id'),nullable = True)
    linkPrecedence = db.Column(Enum('primary','secondary',name = 'link_Precedence'),nullable = False)
    createdAT = db.Column(DateTime, default = datetime.now())
    updatedAT = db.Column(DateTime, nullable = True)
    deletedAT = db.Column(DateTime, nullable = True)
      
@app.route("/identify", methods = ['POST'])
@limiter.limit('5 per minute')
def identify():
    
    """
    API Endpoint: /identify
    - Accepts JSON input with "email" and "phoneNumber".
    - Identifies and links contacts based on existing records.
    - Creates new primary contact if no match is found.
    - Returns JSON response with linked contact details.
    """
    
    try:
        data = request.get_json()
        email = data['email']
        phoneno = data['phone_number']
        
        #Handling complete empty inputs
        if not email and not phoneno:
            return bad_req(400)
        
        #Fetching exisitng contacts if any
        existing_contacts  = Contact.query.filter((Contact.email == email) | (Contact.phoneNumber == phoneno)).all()
        
        #If there is no existing contacts we create a new one
        if not existing_contacts:
            new_contact = Contact(email = email, phoneNumber = phoneno, linkPrecedence = 'primary', createdAT = datetime.now())
            db.session.add(new_contact)
            db.session.commit()
            return {
                'id' : new_contact.id,
                'phoneNumber' : [new_contact.phoneNumber],
                'email' : [new_contact.email],
                'secondaryContactids' : []
            },200
        
        #Handling_linking of contacts
        primary_col = min(existing_contacts, key = lambda x: x.id) #Determining the oldest primary contact
        secondary_contacts = [c for c in existing_contacts if primary_col.id != c.id] #Find all secondary contacts linked to this primary
        
        #Creating secondary contact entry in case of a common email
        if email and not any(c.email == email for c in existing_contacts):
            new_secondary = Contact(email = email, phoneNumber = None, linkedid = primary_col.id, linkPrecedence = 'secondary')
            db.session.add(new_secondary)
            db.session.commit()
            secondary_contacts.append(new_secondary)
            
        #Creating secondary contact entry in case of a common phone number
        if phoneno and not any(c.phoneNumber == phoneno for c in existing_contacts):
            new_secondary = Contact(email = None, phoneNumber = phoneno, linkedid = primary_col.id, linkPrecedence = 'secondary')
            db.session.add(new_secondary)
            db.session.commit()
            secondary_contacts.append(new_secondary)
            
        else:
            for contact in existing_contacts:
                if contact.id != primary_col.id:
                    contact.linkedid = primary_col.id
                    contact.linkPrecedence = 'secondary'
                db.session.commit()
                
        #Building Response
        return {
                'primary_id' : primary_col.id,
                'phoneNumber' : list(set([c.phoneNumber for c in existing_contacts if c.phoneNumber])),
                'email' : list(set([c.email for c in existing_contacts if c.email])),
                'secondary_contact_id' : [sec.id for sec in secondary_contacts]
            },200
        
    except SQLAlchemyError as error:
        logging.error(f"Database Issue: {str(error)}")
        return {"Error" : "Data queued for manual verification."},200
        

#Error handler for empty incomming requests
@app.errorhandler(400)
def bad_req(error):
    return {"Error" : "Unexpected input format"} , 400 


@app.errorhandler(500)
def bad_req(error):
    return {"Error" : "Request processed, awaiting validation"} , 500 
     
    
if __name__=='__main__':
    app.run(debug=True)





















# '''from flask import Flask, render_template, session, request, redirect, jsonify, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from sqlalchemy import String, Integer, ForeignKey
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



# app = Flask(__name__)
# jwt = JWTManager(app)
# app.config['JWT_SECRET_KEY'] = "Hello"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to.db"
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

# class User(db.Model):
#     id = db.Column(Integer, primary_key = True)
#     email = db.Column(String,nullable = False, unique = True)
#     password = db.Column(String,nullable =False)
#     todo = db.relationship("TODO", backref = "user", lazy = True)
    
# class TODO(db.Model):
#     id = db.Column(Integer, primary_key = True)
#     title = db.Column(String, nullable = False)
#     desc = db.Column(String, nullable = False)
#     user_id = db.Column(Integer,ForeignKey("user.id"),nullable = False)


# @app.route("/register", methods = ["POST"])
# def register():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
    
#     if not email or not password:
#         return {"Message" : "Invalid Username or Password"},400
    
#     if User.query.filter_by(email=email).first():
#         return {"Message" : "User already exists"},409
    
    
#     hashed = bcrypt.generate_password_hash(password).decode("utf-8")
#     verify_user = User(email = email, password = hashed)
    
#     db.session.add(verify_user)
#     db.session.commit()
#     return {"Message" : "User registered successfully"},201

# @app.route("/login", methods = ["GET", "POST"])
# def login():
#     data  =request.get_json()
#     email = data["email"]
#     password = data["password"]
    
#     if not email or not password:
#         return {"Message" : "Invalid Username or Password"},400
    
#     verify_user: User = User.query.filter_by(email=email).first()
#     if not verify_user or not bcrypt.check_password_hash(verify_user.password,password):
#         return {"Message" : "Invalid Credentials"},401
    
    
#     access_token = create_access_token(identity=email)
#     return {"Access Token" : access_token},200
    
# @app.route("/create" , methods = ["GET", "POST"])
# @jwt_required()
# def create():
#     current_user = get_jwt_identity()
#     info = request.get_json()
#     title = info["title"]
#     desc = info["desc"]
    
#     user: User= User.query.filter_by(email=current_user).first()
#     if not user:
#         return {"Message" : "User not found"}
    
#     if not title:
#         return {"Message" : "No title, Please enter title"},400
    
#     new_todo = TODO(title = title, desc =desc, user_id = user.id) 
#     db.session.add(new_todo)
#     db.session.commit()
    
#     return {"Message" : f"Todo Created Successfully , id : {new_todo.id}"}

# @app.route("/edit/<int:todo_id>", methods=["POST"])
# @jwt_required()
# def edit(todo_id):
#     current_user = get_jwt_identity()
#     info = request.get_json()
#     title = info["title"]
#     desc = info["desc"]
    
#     user : User = User.query.filter_by(email=current_user).first()
#     if not user:
#         return{"Message" : "User doesn't exist"},404
    
#     todo : TODO= TODO.query.filter_by(id = todo_id, user_id = user.id).first()
    
#     if not todo:
#         return {"Message" : "Todo not found"},404
    
#     todo.title = title
#     todo.desc = desc
#     db.session.commit()
#     return {"Message" : "Todo updated successfully"}
    
    
# @app.route("/delete/<int:todo_id>", methods = ["POST", "GET"])
# @jwt_required()
# def delete(todo_id):
#     current_user = get_jwt_identity()
#     user :User  = User.query.filter_by(email=current_user).first()
    
#     if not user:
#         return {"Message" : "User doesn't exist"}, 404
    
#     todo = TODO.query.filter_by(id = todo_id, user_id = user.id).first()
#     if not todo:
#         return {"Message" : "Todo deleted succesfully"}
    
#     db.session.delete(todo)
#     db.session.commit()
#     return {"Message" : "Deleted successfully"}
    




    
    
    
    
    




    
# if __name__ == "__main__":
#     app.run(debug=True)
     
#      '''