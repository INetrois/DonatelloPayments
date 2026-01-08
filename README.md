<p align="center">
  <img src="https://img.shields.io/badge/-DonatelloPayments-blue?style=for-the-badge&logo=fastapi&logoColor=white" alt="DonatelloPayments"/>
</p>

---

<p align="center">
  🐍 API that allows you to make payments using Donatello.
</p>

<br>

<h2 align="center">🔹 Features</h2>

- Database Payments saving
- Automatic generation url for Payment
- FastAPI simple API
- Simple config 

<h2 align="center">💻 Installation</h2>

> <a href="https://donatello.to/panel/doc-api">Get your Donatello API token</a>

```bash
git clone https://github.com/INetrois/DonatelloPayments.git
cd DonatelloPayments
cp .env.example .env
nano .env
uv sync
uv run src/app.py
```

<h2 align="center">⚙️ Configuration</h2>

Edit your `.env` file with the following variables:

```env
DATABASE_URL="sqlite+aiosqlite:///./dbs/db.sqlite3"
DONATELLO_TOKEN="<your_donatello_token_here>"
HOST="0.0.0.0"
PORT=8000
DEBUG="false"
```

<h2 align="center">📡 Endpoints</h2>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/payments/` | Get list of all Payments |
| `POST` | `/api/v1/payments/` | Create Payment |
| `POST` | `/api/v1/donatello/` | Generate payment URL |
| `POST` | `/api/v1/donatello/callback/` | Handle Donatello Callback |

<h2 align="center">🚀 Usage</h2>

### Get All Payments

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/payments/' \
  -H 'accept: application/json'
```

### Create Payment

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/payments/?amount=100&description=Default%20Payment' \
  -H 'accept: application/json' \
  -d ''
```

### Generate Payment URL

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/donatello/?payment_id=1' \
  -H 'accept: application/json' \
  -d ''
```

<h2 align="center">📚 API Documentation</h2>

Once the server is running, you can access:

- **Interactive API docs (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative API docs ( ReDoc )**: http://127.0.0.1:8000/redoc
<br>

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/INetrois">INetrois</a>
</p>
