🚀 Gen AI Query API

Welcome to the Gen AI Query API, a lightweight backend service that simulates an AI-powered data query system. This project is built using Flask and PostgreSQL, and is deployed on Render.

📌 Features

🔍 Convert natural language queries to pseudo-SQL

📊 Simulated query processing with mock responses

✅ Query validation with error handling

🔐 Lightweight authentication

🔧 Setup Instructions

1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/gen-ai-query-api.git
cd gen-ai-query-api
```

2️⃣ Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Set Up Environment Variables

Create a .env file and add the following:
```bash
DATABASE_URL=postgresql://your_user:your_password@your_host:your_port/your_database
```

5️⃣ Run Migrations (if using a database)
```bash
flask db upgrade
```
6️⃣ Start the Server
```bash
flask run
```
🚀 API Endpoints

📂 Postman Collection

You can import the Postman collection from the following file: 📎 [Postman Collection](https://raw.githubusercontent.com/sourya258/Natural_Language_to_SQL_API/refs/heads/main/Gen_AI_QUery_API.postman_collection.json)

🌍 Live Deployment

Check out the live API here: 🔗 [Gen AI Query API on Render](https://natural-language-to-sql-api.onrender.com/apidocs/#/)

🛠 Tech Stack

Backend: Python (Flask)

Database: PostgreSQL

Deployment: Render

💡 Feel free to contribute or report any issues! 🚀
