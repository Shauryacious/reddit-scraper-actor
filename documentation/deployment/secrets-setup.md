# Secrets and Environment Variables Setup Guide

This document explains how to set up the required secrets and environment variables for CI/CD pipelines in GitHub Actions.

## Overview

This repository uses GitHub Actions for CI/CD with the following workflows:

- **CI Workflow** (`ci.yml`) - Runs tests and linting (no secrets required)
- **CD Workflow** (`cd.yml`) - Builds and pushes Docker images (requires Docker Hub secrets)
- **Docker Build Test** (`docker-build-test.yml`) - Tests Docker builds (no secrets required)

## Quick Setup Checklist

- [ ] Create Docker Hub account
- [ ] Create Docker Hub repository: `reddit-scraper-actor`
- [ ] Generate Docker Hub Personal Access Token
- [ ] Add `DOCKER_USERNAME` secret to GitHub
- [ ] Add `DOCKER_PASSWORD` secret to GitHub
- [ ] Verify workflow runs successfully

## GitHub Secrets

GitHub Actions workflows require secrets to be configured in your repository settings. Secrets are encrypted and only accessible to workflows.

### How to Add GitHub Secrets

1. Navigate to your GitHub repository
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter the secret name (must match exactly)
5. Enter the secret value
6. Click **Add secret**
7. Repeat for each required secret

**Note:** Once a secret is added, you cannot view its value again. You can only update or delete it.

### Required Secrets

#### Docker Hub Credentials

These secrets are **required** for the CD workflow to build and push Docker images.

| Secret Name | Description | Used By | Example Value |
|------------|-------------|---------|---------------|
| `DOCKER_USERNAME` | Your Docker Hub username | CD workflow | `your-dockerhub-username` |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token | CD workflow | `dckr_pat_xxxxxxxxxxxxx` |

**Security Recommendation:** Always use a Docker Hub [Personal Access Token](https://docs.docker.com/docker-hub/access-tokens/) instead of your password. Tokens can be revoked without changing your password and provide better security.

### Optional Secrets

These secrets are optional and only needed for specific features:

| Secret Name | Description | Used By | When Needed |
|------------|-------------|---------|-------------|
| `CODECOV_TOKEN` | Codecov authentication token | CI workflow | Only if using private Codecov or need upload authentication |
| `APIFY_API_TOKEN` | Apify API token | Future use | If automating Apify actor deployment |

**Note:** The CI workflow uses Codecov but has `fail_ci_if_error: false`, so it will work without a token for public repositories.

## Environment Variables

The CD workflow uses environment variables defined at the workflow level. These are set in `.github/workflows/cd.yml`:

```yaml
env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ secrets.DOCKER_USERNAME }}/reddit-scraper-actor
```

### Workflow Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `REGISTRY` | `docker.io` | Docker registry (Docker Hub) |
| `IMAGE_NAME` | `{DOCKER_USERNAME}/reddit-scraper-actor` | Full Docker image name |

These variables are automatically used by the workflow and don't need to be configured manually. The `IMAGE_NAME` is constructed from the `DOCKER_USERNAME` secret.

## Docker Hub Setup

### Step 1: Create Docker Hub Account

If you don't have a Docker Hub account:

1. Go to [https://hub.docker.com](https://hub.docker.com)
2. Click **Sign Up** (or **Sign In** if you have an account)
3. Complete the registration process
4. Verify your email address if required

### Step 2: Create Repository

1. Log in to Docker Hub
2. Click **Repositories** in the top navigation
3. Click **Create Repository** button
4. Fill in the repository details:
   - **Name**: `reddit-scraper-actor` (must match exactly)
   - **Visibility**: Choose Public or Private
   - **Description**: (Optional) Add a description
5. Click **Create**

**Important:** The repository name must be exactly `reddit-scraper-actor` to match the workflow configuration.

### Step 3: Generate Personal Access Token (Recommended)

For better security, use a Personal Access Token instead of your password:

1. Log in to Docker Hub
2. Click your username in the top right → **Account Settings**
3. Navigate to **Security** tab
4. Click **New Access Token** button
5. Fill in the token details:
   - **Description**: `GitHub Actions CI/CD` (or similar)
   - **Access permissions**: Select **Read & Write** (required for pushing images)
6. Click **Generate**
7. **Copy the token immediately** - you won't be able to see it again!
8. Store it securely - you'll use this as the `DOCKER_PASSWORD` secret

**Token Format:** Docker Hub tokens start with `dckr_pat_` followed by a long string of characters.

### Step 4: Add Secrets to GitHub

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add `DOCKER_USERNAME`:
   - Click **New repository secret**
   - Name: `DOCKER_USERNAME`
   - Value: Your Docker Hub username (e.g., `myusername`)
   - Click **Add secret**
4. Add `DOCKER_PASSWORD`:
   - Click **New repository secret**
   - Name: `DOCKER_PASSWORD`
   - Value: Your Docker Hub Personal Access Token (e.g., `dckr_pat_xxxxxxxxxxxxx`)
   - Click **Add secret**

## Verification

After setting up secrets, verify everything works:

### 1. Check Secrets Are Configured

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Verify both `DOCKER_USERNAME` and `DOCKER_PASSWORD` are listed
3. Ensure they show as "Updated" with recent timestamps

### 2. Trigger the CD Workflow

You can trigger the workflow in several ways:

**Option A: Push to main/master branch**
```bash
git checkout main
git commit --allow-empty -m "Trigger CD workflow"
git push origin main
```

**Option B: Create a version tag**
```bash
git tag v1.0.0
git push origin v1.0.0
```

**Option C: Manual workflow dispatch**
1. Go to **Actions** tab in GitHub
2. Select **CD - Build and Push Docker Image** workflow
3. Click **Run workflow**
4. Choose branch and tag (optional)
5. Click **Run workflow**

### 3. Verify Workflow Success

1. Go to **Actions** tab in GitHub
2. Find the running workflow run
3. Click on it to see job details
4. Verify both jobs complete successfully:
   - ✅ **Build and Push Docker Image**
   - ✅ **Security Scan**

### 4. Verify Docker Image

1. Go to [Docker Hub](https://hub.docker.com)
2. Navigate to your repository: `{username}/reddit-scraper-actor`
3. Verify the image appears with the correct tag:
   - `latest` for main/master branch pushes
   - Branch name for other branch pushes
   - Version tag for tag pushes
4. Check the image was pushed recently

## Troubleshooting

### Common Issues

#### Docker Login Fails

**Error:** `Error response from daemon: Get "https://registry-1.docker.io/v2/": unauthorized`

**Solutions:**
- Verify `DOCKER_USERNAME` matches your Docker Hub username exactly (case-sensitive)
- If using a token, ensure it has **Read & Write** permissions
- Check that the token hasn't expired (tokens can have expiration dates)
- Verify the token format starts with `dckr_pat_`
- Try generating a new token and updating the secret

#### Image Not Pushing

**Error:** `denied: requested access to the resource is denied`

**Solutions:**
- Ensure the repository name in Docker Hub matches exactly: `reddit-scraper-actor`
- Verify the image name format: `{DOCKER_USERNAME}/reddit-scraper-actor`
- Check that you have push access to the repository
- If using an organization, verify your account has write permissions
- Check workflow logs for specific error messages

#### Secret Not Found

**Error:** `Secret not found: DOCKER_USERNAME` or similar

**Solutions:**
- Verify the secret name matches exactly (case-sensitive): `DOCKER_USERNAME` and `DOCKER_PASSWORD`
- Ensure secrets are added at the repository level (not organization level, unless configured)
- Check that you're looking at the correct repository
- Verify you have admin access to the repository (required to manage secrets)

#### Workflow Fails with "No such image"

**Error:** `unable to find the specified image` in security scan

**Solutions:**
- This usually means the image wasn't built/pushed successfully
- Check the `build-and-push` job logs first
- Verify the image tag matches what was actually pushed
- Ensure the security scan job runs after the build job completes

#### Token Expired

**Error:** `authentication required` or `unauthorized`

**Solutions:**
- Generate a new Personal Access Token in Docker Hub
- Update the `DOCKER_PASSWORD` secret with the new token
- Re-run the workflow

### Getting Help

If you continue to experience issues:

1. **Check Workflow Logs:**
   - Go to **Actions** → Select the failed workflow run
   - Expand the failed job and step
   - Look for specific error messages

2. **Verify Configuration:**
   - Double-check all secret names match exactly
   - Verify Docker Hub repository exists and is accessible
   - Ensure your Docker Hub account is active

3. **Test Locally:**
   ```bash
   # Test Docker login locally
   docker login -u YOUR_USERNAME -p YOUR_TOKEN
   docker push YOUR_USERNAME/reddit-scraper-actor:test
   ```

## Security Best Practices

### 1. Never Commit Secrets

- **Never** commit secrets, passwords, or tokens to the repository
- All secrets should be stored in GitHub Secrets only
- Add `.env` files to `.gitignore` if you use them locally
- Review commits before pushing to ensure no secrets are included

### 2. Use Personal Access Tokens

- Always prefer tokens over passwords
- Tokens can be revoked without changing your password
- Set appropriate expiration dates (or no expiration for long-term use)
- Use descriptive names for tokens to identify their purpose

### 3. Rotate Secrets Regularly

- Update tokens/passwords periodically (recommended: every 90 days)
- Revoke old tokens when no longer needed
- Monitor Docker Hub for any suspicious activity

### 4. Limit Secret Scope

- Only grant minimum required permissions
- Use repository-specific secrets when possible (not organization-wide)
- Review who has access to repository secrets

### 5. Monitor Workflow Access

- Regularly review workflow runs in the Actions tab
- Check for any unauthorized workflow executions
- Enable branch protection rules for main/master branches

### 6. Use Environment Protection Rules (Optional)

For additional security, you can set up environment protection rules:
1. Go to **Settings** → **Environments**
2. Create a new environment (e.g., "production")
3. Add required reviewers for deployments
4. Restrict which branches can deploy

## Workflow Permissions

The CD workflow requires the following permissions (configured in `.github/workflows/cd.yml`):

| Permission | Purpose | Required For |
|------------|---------|--------------|
| `contents: read` | Read repository code | Checking out code |
| `packages: write` | Push Docker images | Pushing to Docker Hub |

These permissions are set at the job level and should work by default for most repositories. If you encounter permission issues:

1. Check repository settings → **Actions** → **General**
2. Verify "Workflow permissions" allows read/write access
3. Ensure branch protection rules don't block workflows

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Docker Hub Repository Management](https://docs.docker.com/docker-hub/repos/)

