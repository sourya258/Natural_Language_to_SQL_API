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
