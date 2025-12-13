# CI/CD Setup Guide

This document explains the CI/CD pipeline setup for the Reddit Scraper Actor.

## Overview

The project includes three GitHub Actions workflows:

1. **CI - Tests and Linting** (`.github/workflows/ci.yml`)
   - Runs on every push and pull request
   - Executes unit tests with pytest
   - Performs code linting with flake8, black, and isort
   - Tests against Python 3.11 and 3.12

2. **CD - Build and Push Docker Image** (`.github/workflows/cd.yml`)
   - Runs on pushes to main/master branch and version tags
   - Builds Docker image with multi-platform support (amd64, arm64)
   - Pushes to Docker Hub
   - Performs security scanning with Trivy

3. **Docker Build Test** (`.github/workflows/docker-build-test.yml`)
   - Runs on pull requests
   - Tests that Docker image builds successfully
   - Does not push to registry

## Prerequisites

Before setting up CI/CD, ensure you have:

1. **GitHub Repository**
   - A remote GitHub repository created
   - Repository initialized locally

2. **Docker Hub Account**
   - Account created at [hub.docker.com](https://hub.docker.com)
   - Repository named `reddit-scraper-actor` created
   - See [SECRETS_SETUP.md](./SECRETS_SETUP.md) for details

3. **GitHub Secrets**
   - `DOCKER_USERNAME` - Your Docker Hub username
   - `DOCKER_PASSWORD` - Your Docker Hub password or access token
   - See [SECRETS_SETUP.md](./SECRETS_SETUP.md) for setup instructions

## Initial Setup

### 1. Initialize Git Repository

If not already initialized:

```bash
cd reddit-scraper-actor
git init
git add .
git commit -m "Initial commit: Reddit scraper actor with CI/CD"
```

### 2. Create Remote Repository

Create a new repository on GitHub:

1. Go to [GitHub](https://github.com/new)
2. Name it `reddit-scraper-actor` (or your preferred name)
3. Choose public or private
4. **Do not** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 3. Connect Local to Remote

```bash
git remote add origin https://github.com/YOUR_USERNAME/reddit-scraper-actor.git
git branch -M main
git push -u origin main
```

### 4. Configure GitHub Secrets

Follow the instructions in [SECRETS_SETUP.md](./SECRETS_SETUP.md) to add:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

### 5. Verify Setup

1. Push a commit to trigger workflows:
   ```bash
   git add .
   git commit -m "Add CI/CD workflows"
   git push
   ```

2. Check GitHub Actions:
   - Go to your repository on GitHub
   - Click the **Actions** tab
   - You should see workflows running

3. Verify Docker image:
   - Go to [Docker Hub](https://hub.docker.com)
   - Check your repository for the new image

## Workflow Details

### CI Workflow

**Triggers:**
- Push to `main`, `develop`, or `master`
- Pull requests to `main`, `develop`, or `master`

**Jobs:**
- **test**: Runs pytest with coverage on Python 3.11 and 3.12
- **lint**: Runs flake8, black, and isort checks

**Duration:** ~2-5 minutes

### CD Workflow

**Triggers:**
- Push to `main` or `master` branch
- Version tags (e.g., `v1.0.0`)
- Manual workflow dispatch

**Jobs:**
- **build-and-push**: Builds and pushes Docker image
- **security-scan**: Scans image for vulnerabilities

**Image Tags:**
- `latest` - Latest main/master branch
- `main` or `master` - Branch name
- `v1.0.0` - Semantic version tags
- `1.0` - Major.minor version
- `1` - Major version

**Duration:** ~5-10 minutes

### Docker Build Test Workflow

**Triggers:**
- Pull requests to `main`, `develop`, or `master`

**Jobs:**
- **test-docker-build**: Builds Docker image without pushing

**Duration:** ~2-3 minutes

## Running Tests Locally

Before pushing, you can run tests locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run linting
flake8 src/ tests/
black --check src/ tests/
isort --check-only src/ tests/
```

## Docker Commands

### Build Locally

```bash
docker build -t reddit-scraper-actor:local .
```

### Run Locally

```bash
docker run --rm reddit-scraper-actor:local
```

### Test with Input

```bash
docker run --rm \
  -v $(pwd)/test-input.json:/apify/INPUT.json \
  reddit-scraper-actor:local
```

## Troubleshooting

### Workflows Not Running

- Check that workflows are in `.github/workflows/` directory
- Verify YAML syntax is correct
- Ensure you've pushed to the correct branch

### Docker Build Fails

- Check Dockerfile syntax
- Verify all dependencies are in requirements.txt
- Review build logs in GitHub Actions

### Tests Failing

- Run tests locally to reproduce issues
- Check Python version compatibility
- Verify all test dependencies are installed

### Secrets Not Working

- Verify secret names match exactly (case-sensitive)
- Check that secrets are set in repository settings
- Ensure Docker Hub credentials are correct

## Best Practices

1. **Always run tests locally before pushing**
   ```bash
   pytest tests/ -v
   ```

2. **Keep workflows updated**
   - Update action versions periodically
   - Review security advisories

3. **Monitor workflow runs**
   - Check Actions tab regularly
   - Fix failing workflows promptly

4. **Use semantic versioning**
   - Tag releases with `v1.0.0` format
   - This triggers CD workflow automatically

5. **Review security scans**
   - Check Trivy scan results
   - Update dependencies with vulnerabilities

## Next Steps

1. ✅ Set up GitHub repository
2. ✅ Configure GitHub secrets
3. ✅ Create Docker Hub repository
4. ✅ Push code and verify workflows
5. 🔄 Monitor CI/CD pipelines
6. 🔄 Set up branch protection rules (optional)
7. 🔄 Configure deployment to Apify (optional)

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Apify Actor Documentation](https://docs.apify.com/actors)

