# FitBuddy-2 🏋️‍♂️

FitBuddy-2 is an AI-powered fitness web application built using **FastAPI**, **Jinja2**, and **Google Generative AI**.
The app helps users get personalized fitness insights, track users, and manage fitness-related data through a simple web interface.

---

## 🚀 Live Demo

👉 **Open the App:**
https://fitbuddy-2-9c7y.onrender.com

*(Note: The free Render instance may take 30–60 seconds to wake up after inactivity.)*

---

# 🛠 Tech Stack

* Python
* FastAPI
* Jinja2 Templates
* SQLAlchemy
* Google Generative AI
* Uvicorn
* HTML / CSS / JavaScript

---

# 📂 Project Structure

```
FitBuddy-2
│
├── app
│   ├── main.py
│   ├── models
│   ├── routes
│   ├── static
│   └── templates
│
├── requirements.txt
├── runtime.txt
└── README.md
```

---

# ⚙️ Local Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ayushmishragn-sudo/FitBuddy-2.git
cd FitBuddy-2
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

# ☁️ Deploy on Render

This project is deployed using **Render**.

### Step 1 — Push project to GitHub

Make sure your project is available on GitHub.

---

### Step 2 — Create Web Service on Render

Go to:

https://dashboard.render.com

Click:

```
New → Web Service
```

Connect your GitHub repository.

---

### Step 3 — Configure Deployment

Use the following settings:

**Environment**

```
Python
```

**Build Command**

```
pip install -r requirements.txt
```

**Start Command**

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### Step 4 — Deploy

Click **Create Web Service**.

Render will automatically:

* Clone the repository
* Install dependencies
* Start the FastAPI server

---

# 🌍 Live Deployment

Once deployed, your app will be available at:

https://fitbuddy-2-9c7y.onrender.com

---

# ⚠️ Notes

* Render free services may **sleep after inactivity**.
* The first request after inactivity may take **30–60 seconds**.

---

# 👨‍💻 Author

**Ayush Mishra**

GitHub:
https://github.com/ayushmishragn-sudo

---

⭐ If you like this project, consider giving it a star!
