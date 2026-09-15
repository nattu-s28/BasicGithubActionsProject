# 🔧 GitHub Actions — Full Explanation Guide

This document explains, in plain language, **every GitHub Actions workflow**
in this project: what it does, when it runs, and *why* it's structured the
way it is. Read this alongside the actual `.yml` files in
`.github/workflows/`.

---

## 🧠 First — What Is a GitHub Action, Really?

A **workflow** is a YAML file that tells GitHub: *"When X happens, run these
steps on a fresh virtual machine."*

Every workflow has this shape:

```yaml
on: [when to run]        # the trigger
jobs:
  job-name:
    runs-on: ubuntu-latest   # what machine to use
    steps:                   # what to actually do, in order
      - uses: some/action@v1     # reuse someone else's pre-built step
      - run: some-shell-command  # or run your own command
```

This project uses **5 separate workflows**, each responsible for one job —
this is best practice (small, focused workflows) rather than one giant file.

---

## 1️⃣ `ci.yml` — Continuous Integration (Lint & Test)

**Triggers:** every `push` and `pull_request` to `main`.

**What it teaches:** the core idea of CI — automatically checking that code
still works *before* it's trusted.

**What it does, step by step:**
1. Checks out your code (`actions/checkout`).
2. Installs Python — and does this **three times in parallel** using a
   **matrix strategy** (Python 3.10, 3.11, 3.12), so you know your code
   works across versions, not just on your machine.
3. Installs dependencies.
4. Runs **flake8** — catches real errors (undefined names, syntax issues)
   and reports style issues.
5. Runs **black --check** — verifies code formatting is consistent,
   without changing anything (a real `black` run would auto-format; `--check`
   just reports).
6. Runs **pytest** with coverage — actually executes your test suite and
   reports what percentage of your code is tested.
7. Uploads the coverage report as a downloadable **artifact** — visible
   under the workflow run's "Artifacts" section.

**Key concepts demonstrated:** triggers, matrix builds, dependency caching,
artifacts.

---

## 2️⃣ `codeql.yml` — Security Scanning

**Triggers:** push/PR to `main`, **plus a weekly schedule** (`cron`).

**What it teaches:** automated security review. **CodeQL** is GitHub's own
free static-analysis engine — it doesn't just lint style, it looks for real
vulnerability *patterns*: unsafe input handling, injection risks, secrets
accidentally committed, etc.

**Why a schedule too?** Vulnerability databases update constantly. Even if
your code never changes, running this weekly means newly discovered
vulnerability patterns still get checked against your existing code.

**Key concepts demonstrated:** scheduled triggers (`cron`), security
permissions (`security-events: write`), GitHub's native security tooling.

---

## 3️⃣ `docker-publish.yml` — Build & Publish a Docker Image

**Triggers:** push to `main`, or manually via **"Run workflow"** button
(`workflow_dispatch`).

**What it teaches:** packaging an app into a portable container and
publishing it — for free — so anyone can run it with one command.

**What it does:**
1. Logs into **GitHub Container Registry (GHCR)** using the automatically
   provided `GITHUB_TOKEN` secret — you don't create or manage any
   credentials yourself.
2. Builds tags/labels for the image automatically (`latest` + a tag based
   on the commit hash).
3. Uses **Buildx** (Docker's advanced builder) with **layer caching**
   (`cache-from`/`cache-to: type=gha`) so repeat builds are much faster.
4. Pushes the image to `ghcr.io/<your-username>/<your-repo>`.

**Why this matters:** this is genuinely how real companies ship software —
build once in CI, publish a versioned image, deploy that exact image
everywhere.

**Key concepts demonstrated:** `workflow_dispatch` manual triggers,
`permissions` scoping, built-in `secrets.GITHUB_TOKEN`, build caching,
container registries.

---

## 4️⃣ `pages.yml` — Deploy Docs to GitHub Pages (Free Hosting)

**Triggers:** push to `main` that touches the `docs/` folder, or manual.

**What it teaches:** deploying a live, public website for free, directly
from your repository, with zero external hosting accounts.

**What it does:**
1. Checks out the repo.
2. Configures GitHub Pages for this repository.
3. Uploads the `docs/` folder as a deployable artifact.
4. Deploys it — GitHub gives you a live URL:
   `https://<username>.github.io/<repo-name>/`

**Note:** you must flip one switch manually the *first* time — go to
**Settings → Pages → Source → GitHub Actions** — after that, every future
push deploys automatically.

**Key concepts demonstrated:** `concurrency` groups (prevents two deploys
racing each other), `environment` URLs, minimal `permissions`, Pages
deployment actions.

---

## 5️⃣ `release.yml` — Automatic GitHub Releases

**Triggers:** only when you push a **version tag** matching `v*.*.*`
(e.g. `v1.0.0`, `v2.3.1`).

**What it teaches:** tying releases to **semantic version tags** instead of
manually writing release notes in the GitHub UI every time.

**What it does:**
1. Waits for a tag push (not just any commit).
2. Automatically creates a GitHub Release for that tag.
3. Auto-generates release notes by summarizing merged PRs/commits since the
   last release.

**How you trigger it:**
```bash
git tag v1.0.0
git push --tags
```

**Key concepts demonstrated:** tag-based triggers, `contents: write`
permission, third-party marketplace actions (`softprops/action-gh-release`).

---

## 🔁 Bonus: `dependabot.yml` — Not a Workflow, But Related Automation

This isn't technically a GitHub *Action*, but it's GitHub's other major free
automation feature, and it pairs naturally with Actions:

- Every week, Dependabot scans your `requirements.txt` **and** your
  workflow files for outdated versions.
- It opens a **pull request** automatically when an update is available.
- Your `ci.yml` workflow then automatically runs against that PR — so you
  get a tested, ready-to-merge dependency update with zero manual work.

---

## 📊 Summary Table

| Workflow file          | Trigger                          | Purpose                              | Costs money? |
|-------------------------|-----------------------------------|----------------------------------------|---------------|
| `ci.yml`                | push / PR                        | Lint + test the code                   | Free |
| `codeql.yml`            | push / PR / weekly schedule       | Security vulnerability scanning        | Free |
| `docker-publish.yml`    | push to main / manual             | Build & publish Docker image           | Free (GHCR) |
| `pages.yml`             | push to `docs/` / manual          | Deploy live docs website               | Free (Pages) |
| `release.yml`           | version tag push                  | Auto-create GitHub Release             | Free |
| `dependabot.yml`        | weekly schedule                   | Auto-open dependency update PRs        | Free |

---

## 🎓 What to Tell Your Teacher

This project demonstrates the **full lifecycle** a real engineering team
automates:

**Code pushed → tested → linted → security-scanned → containerized →
published → documented on a live site → released with version tags** —
entirely through GitHub Actions, entirely for free, with no external
accounts or paid infrastructure required.
