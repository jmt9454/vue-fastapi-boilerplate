_Planned and supervised with human eyes, generated with AI, and reviewed with a few cups of coffee_

# 🏁 Getting Started with the Boilerplate

Welcome! This guide will help you fork this repository, set up your environment, and get the application running on your machine using VS Code.

## 📦 Prerequisites

Before you start, make sure you have these installed:

- [VS Code (Visual Studio Code)](https://code.visualstudio.com/)
- [Python 3.10+](https://www.python.org/downloads/)
  - Note: When installing on Windows, check the box "Add Python to PATH".
  - Verify installation by opening a terminal and running: python --version and pip --version.
- [Node.js (LTS Version)](https://nodejs.org/)
- [Git](https://git-scm.com/)

---

## 1️⃣ Fork & Clone

1.  **Fork:** Click the **"Fork"** button in the top-right corner of this GitHub page. This creates your own copy of the code.
2.  **Clone:** Open your terminal/command prompt and run:

```bash
# Replace YOUR-USERNAME with your actual GitHub username
git clone [https://github.com/YOUR-USERNAME/vue-fastapi-boilerplate.git](https://github.com/YOUR-USERNAME/vue-fastapi-boilerplate.git)
cd vue-fastapi-boilerplate

# Open in VS Code
code .
```

---

## 2️⃣ Setup the Backend (Python)

We use a tool called **uv** because it is extremely fast and manages virtual environments automatically.

### Install uv (if you don't have it)

**Windows (PowerShell):**

```powershell
pip install uv
```

**Mac / Linux:**

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

### Setup the Environment

Open a terminal in VS Code (`Ctrl`+`` ` ``) and run:

```bash
cd backend

# Create the virtual environment
uv venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install libraries from pyproject.toml
uv pip install -r pyproject.toml
```

### Create the Database

The app needs a database to start. We use **Alembic** to create it.

```bash
# Create your .env file
cp .env.example .env
# (On Windows, manually copy and rename .env.example to .env)

# Create the tables in local.db
alembic upgrade head
```

---

## 3️⃣ Setup the Frontend (Vue.js)

Open a **NEW** terminal (Click the `+` icon in the VS Code terminal panel).

```bash
# Navigate to the frontend
cd frontend

# Install dependencies
npm install
```

---

## 🚀 Run the App (The "Two Terminal" Method)

To work on this project, you need two servers running at the same time:

1.  **FastAPI (Backend)** running on port `8000`.
2.  **Vue (Frontend)** running on port `5173`.

### Terminal 1 (Backend)

Make sure you are in the `backend` folder and your venv is active (`(backend)` should appear in the prompt).

```bash
uvicorn app.main:app --reload
```

_You should see: `Application startup complete.`_

### Terminal 2 (Frontend)

Click the Split Terminal icon (or press `Ctrl` + `\`) to open a side-by-side terminal. Make sure you are in the `frontend` folder.

```bash
npm run dev
```

_You should see: `Local: http://localhost:5173/`_

---

## 🌐 Verify It Works

1.  Open your browser to [http://localhost:5173](https://www.google.com/search?q=http://localhost:5173).
2.  You should see the "System Status" page.
3.  Click **"Check Connection"**.
4.  If it says **"Backend is running\!"**, you are ready to code\!

---

## 🛡️ Key Concept: Environment Safety

It is important to understand where your data lives so you don't accidentally delete real user data.

### 💻 Local Environment (Safe Zone)

- **Frontend:** `localhost:5173`
- **Backend:** `localhost:8000`
- **Database:** SQLite (`local.db`)

> **What this means:** When you run the app on your laptop, it uses a local file for the database. You can delete, drop, or break this database as much as you want. It cannot touch the production data.

### ☁️ Cloud Environment (Danger Zone)

- **Frontend:** `your-app.vercel.app`
- **Backend:** `your-app.onrender.com`
- **Database:** PostgreSQL (Neon/Railway)

> **What this means:** When you push code to GitHub and it deploys to dev or main, the boilerplate automatically detects it is running in the cloud. It switches from SQLite to PostgreSQL.

**Safety Mechanism:** The app uses the `DATABASE_URL` environment variable to decide. Locally, it points to a file. In the cloud, it points to a server. This prevents local tests from "nuking" production.

---

## ☁️ Setting up Cloud Databases (Neon)

When you are ready to deploy to the cloud (Render/Railway/Vercel), you need a real PostgreSQL database. We recommend **Neon.tech** because it supports "Branches" (like Git) for your data.

1.  **Sign Up:** Go to [Neon.tech](https://neon.tech) and sign up (GitHub login is easiest).
2.  **Create Your Project:**
    - Name it `university-app` (or whatever you like).
    - Region: Choose one close to you (e.g., US East).
3.  **Get Your PROD Connection String:**
    - Ensure the branch is selected as **main** (This is your Production DB).
    - Click **Copy** on the Connection String.
    - > **Important:** If it starts with `postgres://`, change it to `postgresql://` (add the 'ql') when adding to Render.
    - Save this\! You will use it as `DATABASE_URL`.
4.  **Create Your DEV Database (Branching):**
    - Click "Branches" -\> "New Branch".
    - Name it `dev`.
    - Save the new Connection String. This is for your separate "Dev" deployment.

---

## 🚀 Deploying the Backend (Render)

We use [Render.com](https://render.com) for Python applications.

### 0\. Pre-Flight Check (Crucial\!)

Render does not know about `uv` or `pyproject.toml` by default. You must generate a standard requirements file. Run this in your `backend/` folder:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

**Commit and Push this new file to GitHub.**

### 1\. Create Web Service

Go to Render Dashboard -\> **New +** -\> **Web Service**. Connect your GitHub repository.

### 2\. Configuration Settings

Use these exact settings:

- **Name:** `my-app-backend`
- **Root Directory:** `backend` (⚠️ IMPORTANT: If you miss this, it will crash)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

> The `alembic upgrade head` part ensures your database tables are created automatically on every deploy.

### 3\. Environment Variables

Scroll down to the **Environment Variables** section and add:

- `PYTHON_VERSION`: `3.11.0`
- `DATABASE_URL`: (Paste your Neon connection string here. Remember to change `postgres://` to `postgresql://`)
- `SECRET_KEY`: (Any random string)
- `ALLOW_ORIGINS`: `*` (You will update this later with your frontend URL)

### 4\. Deploy

Click **Create Web Service**. When it says "Live", copy the URL (e.g., `https://my-app.onrender.com`).

---

## 🌐 Deploying the Frontend (Vercel)

We use [Vercel](https://vercel.com) to host the Frontend.

1.  **Create Project:** Go to Vercel, click "Add New..." -\> Project, and import your repository.
2.  **Configuration:**
    - **Framework Preset:** Vue.js
    - **Root Directory:** Click "Edit" and select `frontend`.
3.  **Environment Variables:**
    - Name: `VITE_API_URL`
    - Value: (Paste your Render Backend URL here, e.g., `https://my-app.onrender.com`)
    - > **Note:** Do NOT add a trailing slash `/` at the end.
4.  **Deploy:** Click Deploy.

### 5\. 🚨 CRITICAL: Fix CORS on Render

Right now, your frontend cannot talk to your backend because of security settings.

1.  Copy your new Vercel URL (e.g., `https://university-app.vercel.app`).
2.  Go back to Render Dashboard -\> Backend Service -\> Environment.
3.  Find `ALLOW_ORIGINS`.
4.  Change the value from `*` to your specific Vercel URL.
5.  **Save Changes.** Render will restart.

---

## 🧪 Advanced: Deploying a "Dev" Environment

In professional software, we never push directly to `main`. We push to a `dev` branch first.

### 1\. Create the Git Branch

```bash
git checkout -b dev
git push -u origin dev
```

### 2\. Create a Separate Backend (Render)

Create a **Second Web Service** on Render.

- **Name:** `my-app-backend-dev`
- **Branch:** Select `dev` (This is the magic step).
- **Environment Variables:**
  - `DATABASE_URL`: Paste the **DEV** connection string from Neon.
  - `ALLOW_ORIGINS`: `*` (Since Vercel Dev URLs change, `*` is safest for the Dev backend).

### 3\. Configure the Frontend (Vercel)

Vercel handles dev environments using "Preview Deployments".

1.  Go to your Vercel Project Settings -\> Environment Variables.
2.  Add New Variable:
    - **Name:** `VITE_API_URL`
    - **Value:** `https://my-app-backend-dev.onrender.com` (Your DEV Backend URL).
    - **Select Environments:** Uncheck "Production". Check **"Preview"** and **"Development"**.

### 4\. The Result

- **Users on main:** Vercel uses the Production Backend -\> Main DB.
- **You on dev:** Vercel uses the Dev Backend -\> Dev DB.

---

## 🆘 Common Issues

- **"uv is not recognized":** Restart VS Code after installing uv.
- **"ModuleNotFoundError: No module named 'app'":** You are likely running uvicorn from outside the backend folder. Make sure you `cd backend` first.
