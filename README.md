# Identity Reconciliation API

This API consolidates contact information across multiple purchases by linking duplicate records using email and phone numbers.

## 🚀 Features
- Create primary and secondary contact records.
- Auto-link duplicate identities.
- Provides structured JSON responses.
- Secure and optimized database queries.

## 📂 Tech Stack
- **Flask** (API framework)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM)
- **pytest** (Testing)

## 📌 Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/identity-reconciliation-api.git
   cd identity-reconciliation-api

2. Set Up Virtual Environment

   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows

3. Install Dependencies

   pip install -r requirements.txt

4. Set Up PostgreSQL Database

   Create a PostgreSQL database (contact_db).
   
   Update app.config['SQLALCHEMY_DATABASE_URI'] in app.py with your DB credentials.


5. Run Database Migrations
   
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

6. Run the Application

   python app.py

7. Run Tests

   pytest test_identity.py


📌 API Usage

POST /identify

Request:

{
  "email": "doc@example.com",
  "phoneNumber": "+1234567890"
}

Response:

{
  "primaryContactId": 1,
  "emails": ["doc@example.com"],
  "phoneNumbers": ["+1234567890"],
  "secondaryContactIds": []
}

📝 Author

Sourya Ghosh

www.linkedin.com/in/sourya-ghosh-8a6206354
