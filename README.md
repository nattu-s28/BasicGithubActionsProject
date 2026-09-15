# 📝 Todo API — Python + FastAPI + Full GitHub Actions Pipeline

A simple, beginner-friendly **Todo REST API** built with **Python and FastAPI**,
wired up with a complete **GitHub Actions CI/CD pipeline** — testing, linting,
security scanning, Docker publishing, and free deployment.

This project was built as a learning project to show *every commonly used
type* of GitHub Action in one place. For a full breakdown of what each
workflow does and why, see **[GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md)**.

---

## 📂 Project Structure

```
todo-api-project/
├── app/
│   ├── __init__.py
│   └── main.py                # FastAPI app (all routes live here)
├── tests/
│   ├── __init__.py
│   └── test_main.py           # Pytest test suite
├── docs/
│   └── index.html             # Static docs page deployed to GitHub Pages
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Lint + test on every push/PR
│   │   ├── codeql.yml          # Security vulnerability scanning
│   │   ├── docker-publish.yml  # Build & push Docker image (free registry)
│   │   ├── pages.yml           # Deploy docs/ to GitHub Pages (free hosting)
│   │   └── release.yml         # Auto-create GitHub Releases on version tags
│   └── dependabot.yml          # Auto-updates dependencies weekly
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # + testing/linting dependencies
├── Dockerfile
├── .dockerignore
├── .flake8
├── .gitignore
├── README.md                   # You are here
└── GITHUB_ACTIONS_GUIDE.md     # Deep dive into every workflow
```

---

## 🚀 Quick Start — Run Locally

**Requirements:** Python 3.10+ installed on your machine.

```bash
# 1. Clone your repository (after you've pushed this project to GitHub)
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload
```

The API is now running at **http://127.0.0.1:8000**

Open **http://127.0.0.1:8000/docs** in your browser — FastAPI automatically
generates an interactive Swagger UI where you can test every endpoint by
clicking buttons, no extra tools needed.

---

## 🔌 API Endpoints

| Method | Endpoint        | Description          |
|--------|-----------------|-----------------------|
| GET    | `/`             | Health check          |
| GET    | `/todos`        | List all todos        |
| POST   | `/todos`        | Create a new todo     |
| GET    | `/todos/{id}`   | Get a single todo     |
| PUT    | `/todos/{id}`   | Update a todo         |
| DELETE | `/todos/{id}`   | Delete a todo         |

**Example — create a todo with curl:**
```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish my GitHub Actions project", "done": false}'
```

---

## 🧪 Running Tests Locally

```bash
pip install -r requirements-dev.txt
pytest -v
```

To also see a coverage report (how much of your code is tested):

```bash
pytest --cov=app --cov-report=term-missing
```

To check code style before pushing (the same checks CI will run):

```bash
flake8 app tests
black --check app tests
```

---

## 🐳 Running with Docker

```bash
# Build the image locally
docker build -t todo-api .

# Run it
docker run -p 8000:8000 todo-api
```

Visit **http://127.0.0.1:8000/docs** — same app, now running inside a
container.

Once you push to GitHub, the `docker-publish.yml` workflow automatically
builds this same image and publishes it for free to **GitHub Container
Registry (GHCR)**. Anyone can then pull it with:

```bash
docker pull ghcr.io/<your-username>/<your-repo-name>:latest
```

---

## ☁️ How This Project Deploys "For Free"

This project uses **only free GitHub-native infrastructure** — no credit
card, no external accounts needed:

1. **GitHub Actions** — 2,000 free build minutes/month on public repos
   (actually unlimited/free for public repos).
2. **GitHub Container Registry (GHCR)** — free Docker image hosting,
   authenticated automatically using GitHub's built-in token.
3. **GitHub Pages** — free static website hosting for the `docs/` folder.

No secrets, API keys, or paid services are required to get the whole
pipeline running end-to-end.

> 💡 If you later want to deploy the *live API* itself (not just docs) to a
> public URL, free options that plug into GitHub Actions include
> [Render](https://render.com), [Railway](https://railway.app), or
> [Fly.io](https://fly.io) — each has a free tier and a "deploy hook" you
> can call from a workflow. That's an optional next step, not required for
> this project to work.

---

## ⚙️ Step-by-Step: Push This Project to GitHub and Watch It Deploy

1. **Create a new repository** on GitHub (public, so Actions minutes are
   unlimited and free).
2. **Push this project:**
   ```bash
   cd todo-api-project
   git init
   git add .
   git commit -m "Initial commit: Todo API with full CI/CD pipeline"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
3. Go to the **"Actions"** tab of your repository on GitHub. You'll see
   `CI - Lint & Test`, `CodeQL Security Scan`, and `Build & Publish Docker
   Image` running automatically.
4. **Enable GitHub Pages:** Go to **Settings → Pages → Build and
   deployment → Source**, select **"GitHub Actions"**. Push again (or
   re-run the `Deploy Docs to GitHub Pages` workflow manually) and your
   docs site goes live at:
   `https://<your-username>.github.io/<your-repo-name>/`
5. **Create your first release** (optional):
   ```bash
   git tag v1.0.0
   git push --tags
   ```
   Watch the `Create GitHub Release` workflow build a release automatically.

---

## 📖 Learn More

Read **[GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md)** for a full,
teacher-friendly explanation of what every single workflow does, why it
exists, and which concepts (triggers, jobs, matrix builds, permissions,
secrets, artifacts) it demonstrates.

---

## 📜 License

Free to use for learning purposes.
