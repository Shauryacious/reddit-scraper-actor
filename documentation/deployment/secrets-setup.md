# Secrets Setup Guide

This document explains how to set up the required secrets for CI/CD pipelines in GitHub and Docker Hub.

## GitHub Secrets

GitHub Actions workflows require the following secrets to be configured in your repository settings.

### How to Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the exact name listed below

### Required Secrets

#### Docker Hub Credentials

| Secret Name | Description | Example |
|------------|-------------|---------|
| `DOCKER_USERNAME` | Your Docker Hub username | `your-dockerhub-username` |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token | `dckr_pat_xxxxxxxxxxxxx` |

**Note:** For better security, use a Docker Hub [Personal Access Token](https://docs.docker.com/docker-hub/access-tokens/) instead of your password.

### Optional Secrets (for future use)

If you plan to add additional integrations, you may need:

| Secret Name | Description |
|------------|-------------|
| `APIFY_API_TOKEN` | Apify API token (if needed for actor deployment) |
| `CODECOV_TOKEN` | Codecov token (if using private codecov) |

## Docker Hub Setup

### 1. Create Docker Hub Account

If you don't have a Docker Hub account:
1. Go to [https://hub.docker.com](https://hub.docker.com)
2. Sign up for a free account
3. Verify your email address

### 2. Create Repository

1. Log in to Docker Hub
2. Click **Create Repository**
3. Set the repository name to: `reddit-scraper-actor`
4. Set visibility (Public or Private)
5. Click **Create**

### 3. Generate Access Token (Recommended)

Instead of using your password, generate a Personal Access Token:

1. Go to Docker Hub → **Account Settings** → **Security**
2. Click **New Access Token**
3. Give it a description (e.g., "GitHub Actions CI/CD")
4. Set permissions (Read & Write for push access)
5. Copy the token immediately (you won't see it again)
6. Use this token as `DOCKER_PASSWORD` in GitHub secrets

## Verification

After setting up secrets, verify they work:

1. Push a commit to the `main` or `master` branch
2. Go to **Actions** tab in GitHub
3. Check that the CD workflow runs successfully
4. Verify the Docker image appears in your Docker Hub repository

## Troubleshooting

### Docker Login Fails

- Verify `DOCKER_USERNAME` matches your Docker Hub username exactly
- If using a token, ensure it has write permissions
- Check that the token hasn't expired

### Image Not Pushing

- Ensure the repository name in Docker Hub matches: `reddit-scraper-actor`
- Verify the image name format: `{DOCKER_USERNAME}/reddit-scraper-actor`
- Check workflow logs for specific error messages

### Permission Denied

- Ensure your Docker Hub account has permission to push to the repository
- If using an organization, verify you have push access

## Security Best Practices

1. **Never commit secrets to the repository**
   - All secrets should be stored in GitHub Secrets
   - Add `.env` files to `.gitignore`

2. **Use Personal Access Tokens**
   - Prefer tokens over passwords
   - Tokens can be revoked without changing your password
   - Set appropriate expiration dates

3. **Rotate secrets regularly**
   - Update tokens/passwords periodically
   - Revoke old tokens when no longer needed

4. **Limit secret scope**
   - Only grant minimum required permissions
   - Use repository-specific secrets when possible

## Workflow Permissions

The CD workflow requires the following permissions:
- `contents: read` - To checkout code
- `packages: write` - To push Docker images

These are configured in the workflow file and should work by default for most repositories.

