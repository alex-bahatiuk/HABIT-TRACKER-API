# 🌱 Habit Tracker

Habit Tracker is a full-stack application for creating habits, tracking daily progress,
and building consistency over time.

The project includes:

- 🐍 FastAPI backend
- ⚛️ React web frontend
- 📱 Native Android application written in Kotlin
- 🐘 PostgreSQL database
- 🐳 Docker support
- 🔐 JWT authentication

---

## ✨ Features

- User registration and login
- JWT-based authentication
- Create and delete habits
- Mark habits as completed
- Undo completed habits
- Daily habit status
- Habit history
- Progress tracking
- Habit categories and recommendations
- Android mobile client
- Web client

---

## 🏗 Project structure

```text
Habit-Tracker-API/
│
├── app/                     # FastAPI backend
├── habit-tracker-frontend/  # React frontend
├── android-app/             # Android Kotlin application
├── tests/                   # Backend tests
├── Dockerfile
├── compose.yml
├── requirements.txt
└── README.md

🛠 Tech stack
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
Pydantic
JWT authentication
Pytest
Web
React
Vite
JavaScript
Axios
Android
Kotlin
Jetpack Compose
Retrofit
ViewModel
Coroutines
Infrastructure
Docker
Docker Compose
Git
GitHub

🚀 Running the backend locally
1. Create a virtual environment
python -m venv .venv
2. Activate it

Windows:

.venv\Scripts\activate

Linux/macOS:

source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Start the API
uvicorn app.main:app --reload

API documentation:

http://127.0.0.1:8000/docs

🐳 Docker

The project can also be started with Docker Compose:

docker compose up --build

📱 Android application

The native Android client is located in:

android-app/

Open this directory in Android Studio:

Habit-Tracker-API/android-app

The application communicates with the FastAPI backend using Retrofit.

🌐 Web application

The React frontend is located in:

habit-tracker-frontend/

Install dependencies:

npm install

Run development server:

npm run dev
🔐 Authentication

Protected API endpoints use Bearer token authentication.

Authorization: Bearer <access_token>

After login, the backend returns an access token which is used by both the web and
Android clients.

🧪 Tests

Run backend tests with:

pytest
📌 Project status

Habit Tracker is under active development.

Current focus:

improving the Android application
habit statistics
streak tracking
progress visualization
personalized habit recommendations
👨‍💻 Author

Developed by Alex(Dmytro) Bahatiuk

GitHub: alex-bahatiuk

