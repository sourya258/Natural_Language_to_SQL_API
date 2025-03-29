# 🧠 Natural Language to SQL API

This Flask-based API converts simple natural language queries into SQL statements and executes them on a connected PostgreSQL database. It also provides Swagger-based API documentation for easy testing.

---

## 🚀 Features

- 🔁 Converts natural language queries into SQL
- 📊 Executes SQL queries and returns results from PostgreSQL
- ✅ Validates if a query is supported
- 🔍 Returns SQL translation without execution (Explain endpoint)
- 📘 Swagger UI for API documentation and testing

---

## 🛠️ Technologies Used

- Python & Flask  
- PostgreSQL  
- Flasgger (Swagger UI)  
- psycopg2  
- python-dotenv

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a `.env` file

Add your PostgreSQL credentials in a `.env` file:
```
DB_NAME=your_database
DB_USER=your_username
DB_PASS=your_password
DB_PORT=5432
DB_HOST=your_host
```

> ⚠️ **Do NOT commit `.env` to GitHub.** It should be listed in `.gitignore`.

---

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

### 4. Run the App
```bash
python main.py
```

---

## 🧪 API Endpoints

### `POST /query`
Executes the translated SQL query.

**Input:**
```json
{ "query": "get total sales" }
```

**Response:**
```json
{ "result": [{"sum": 4200}] }
```

---

### `POST /explain`
Returns the SQL query without executing it.

---

### `POST /validate`
Checks if the natural language query is supported.

---

## 🧬 Sample Supported Queries

- `show all customers`
- `get total sales`
- `list top 5 products`

---

## 🌐 Swagger Documentation

Once the app is running, visit:
```
http://localhost:5000/apidocs
```

---

## 📂 File Structure

```
├── main.py           # Main Flask app
├── requirements.txt  # Project dependencies
├── Procfile          # For deployment (e.g. Heroku)
├── .env              # Environment variables (DO NOT COMMIT)
├── .gitignore        # Ignore .env and __pycache__ etc.
```

---

## 📌 Notes

- This app assumes a table named `mock_data` with fields like `price`, `quantity`, etc.
- Extend the `convert_to_sql()` dictionary to support more natural language queries.

---

## 📤 Deployment

You can deploy this to services like **Heroku**, **Render**, or **Railway**. Make sure to set the same environment variables in their respective dashboard.

---
