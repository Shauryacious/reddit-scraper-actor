# CI/CD Quick Start

This repository includes complete CI/CD setup with GitHub Actions and Docker Hub integration.

## 🚀 Quick Setup (5 minutes)

### 1. Create GitHub Repository

```bash
# On GitHub.com, create a new repository named 'reddit-scraper-actor'
# Don't initialize with README, .gitignore, or license
```

### 2. Initialize and Push

```bash
cd reddit-scraper-actor
git add .
git commit -m "Initial commit: Reddit scraper actor with CI/CD"
git remote add origin https://github.com/YOUR_USERNAME/reddit-scraper-actor.git
git branch -M main
git push -u origin main
```

Or use the setup script:
```bash
./setup_git.sh
# Follow the prompts, then:
git add .
git commit -m "Initial commit: Reddit scraper actor with CI/CD"
git push -u origin main
```

### 3. Create Docker Hub Repository

1. Go to [hub.docker.com](https://hub.docker.com)
2. Create repository: `reddit-scraper-actor`
3. Set visibility (Public/Private)

### 4. Configure GitHub Secrets

Go to: **Repository Settings** → **Secrets and variables** → **Actions**

Add these secrets:

| Secret Name | Value |
|------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub password or [access token](https://docs.docker.com/docker-hub/access-tokens/) |

### 5. Verify

1. Push a commit to trigger workflows
2. Check **Actions** tab - workflows should run
3. Check Docker Hub - image should appear

## 📚 Documentation

- **[cicd-setup.md](./cicd-setup.md)** - Detailed CI/CD documentation
- **[secrets-setup.md](./secrets-setup.md)** - Secrets and environment variables configuration guide

## 🧪 Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

## 🐳 Docker Commands

```bash
# Build locally
docker build -t reddit-scraper-actor:local .

# Run locally
docker run --rm reddit-scraper-actor:local
```

## 📋 What's Included

✅ **GitHub Actions Workflows:**
- CI: Tests and linting on every push/PR
- CD: Docker build and push on main branch
- Docker build test on PRs

✅ **Test Suite:**
- Unit tests for helpers
- Unit tests for Reddit service
- pytest configuration

✅ **Docker Integration:**
- Multi-platform builds (amd64, arm64)
- Security scanning with Trivy
- Automated version tagging

✅ **Code Quality:**
- **Black**: Code formatting (enforced in CI)
- **isort**: Import sorting (enforced in CI)
- **flake8**: Static analysis and linting
- **pytest**: Test coverage reporting

**Note:** All code must be formatted with Black before committing. The CI pipeline will fail if code is not properly formatted. See [Code Formatting Guide](../development/code-formatting.md) for details.

## 🔧 Troubleshooting

**Workflows not running?**
- Check `.github/workflows/` directory exists
- Verify YAML syntax
- Ensure you pushed to correct branch

**Docker push failing?**
- Verify secrets are set correctly
- Check Docker Hub repository exists
- Review workflow logs

**Tests failing?**
- Run `pytest tests/ -v` locally
- Check Python version (3.11+)
- Install dependencies: `pip install -r requirements.txt`

## 📞 Need Help?

1. Check [cicd-setup.md](./cicd-setup.md) for detailed docs
2. Review GitHub Actions logs
3. Check [secrets-setup.md](./secrets-setup.md) for secrets and environment variables setup

