# Apify Deployment Guide

This guide walks you through deploying your Reddit Scraper Actor to the Apify platform.

## Prerequisites

Before deploying, ensure you have:

1. ✅ **Apify Account** - Sign up at [apify.com](https://apify.com) if you haven't already
2. ✅ **Apify CLI Installed** - Install globally: `npm install -g apify-cli`
3. ✅ **Logged into Apify** - Run `apify login` to authenticate
4. ✅ **Code Pushed to GitHub** - Your code is already on GitHub
5. ✅ **Docker Image Built** - Your Docker image is on Docker Hub
6. ✅ **API Token Ready** - For automatic deployment, you'll need an Organization API token (see [Secrets Setup Guide](./secrets-setup.md))

## Deployment Methods

You have two options for deploying to Apify:

### Method 1: Using Apify CLI (Recommended for First Deployment)

This method gives you full control and is great for initial setup.

#### Step 1: Verify Apify CLI Setup

```bash
# Check if CLI is installed
apify --version

# Login to Apify (opens browser for authentication)
apify login

# Verify you're logged in
apify info
```

#### Step 2: Navigate to Actor Directory

```bash
cd reddit-scraper-actor
```

#### Step 3: Verify Actor Configuration

Before pushing, ensure your `.actor/actor.json` is correctly configured:

**Important Configuration Notes:**
- **Version Format**: Must be `MAJOR.MINOR` (e.g., `1.0`), NOT `MAJOR.MINOR.PATCH` (e.g., `1.0.0`)
- **Storages Section**: Do NOT include a `storages` section in `actor.json` - Apify manages storage automatically
- **Entrypoint**: Must match your main Python file (e.g., `main.py`)

Example `actor.json`:
```json
{
  "actorSpecification": 1,
  "name": "reddit-scraper",
  "version": "1.0",
  "title": "Reddit Scraper",
  "description": "Scrapes Reddit posts...",
  "defaultRunTimeoutSecs": 3600,
  "defaultMemoryMbytes": 4096,
  "defaultCpuUnits": 1024,
  "dockerfileFile": "Dockerfile",
  "readme": "README.md",
  "runtimeType": "PYTHON",
  "runtimeVersion": "3.11",
  "entrypoint": "main.py"
}
```

#### Step 4: Push to Apify

```bash
# Push actor to Apify platform
apify push

# This will:
# 1. Build Docker image on Apify's servers
# 2. Push to Apify's container registry
# 3. Create/update actor in your Apify account
```

**Note:** The first push will create a new actor. Subsequent pushes will update the existing actor.

**Expected Output:**
```
Info: Created Actor with name reddit-scraper on Apify.
Info: Deploying Actor 'reddit-scraper' to Apify.
Run: Updated version 1.0 for Actor reddit-scraper.
Run: Building Actor reddit-scraper
...
Success: Actor was deployed to Apify cloud and built there.
```

#### Step 4: Verify Deployment

1. Go to [Apify Console](https://console.apify.com)
2. Navigate to **Actors** section
3. You should see your "Reddit Scraper" actor
4. Click on it to view details

### Method 2: Using GitHub Actions (Recommended for CI/CD)

This method automatically deploys when you push to GitHub using GitHub Actions.

**Note:** This requires setting up an **Organization API token** in GitHub Secrets. See the [Secrets Setup Guide](./secrets-setup.md) for detailed instructions.

**Important:** Use an **Organization API token** (not Personal) if you want the actor deployed under your organization.

### Method 3: Using Apify's Built-in GitHub Integration (Alternative)

This method uses Apify's native GitHub integration to automatically deploy when you push to GitHub.

#### Step 1: Connect GitHub Repository

1. Go to [Apify Console](https://console.apify.com)
2. Navigate to **Actors** → **Create new**
3. Select **"Connect GitHub repository"**
4. Authorize Apify to access your GitHub account
5. Select your repository: `reddit-scraper-actor`
6. Click **"Connect"**

#### Step 2: Configure Auto-Deploy

1. In the actor settings, go to **"Source code"** tab
2. Enable **"Auto-deploy on push"**
3. Select branch: `main` or `master`
4. Save settings

#### Step 3: Trigger Deployment

```bash
# Make a small change and push
git commit --allow-empty -m "Trigger Apify deployment"
git push
```

The actor will automatically build and deploy when you push to the configured branch.

**Note:** This method uses Apify's built-in integration. For more control and flexibility, use Method 2 (GitHub Actions) with an Organization API token.

## Post-Deployment Configuration

After deploying, configure your actor in the Apify Console:

### 1. Basic Settings

- **Title**: Reddit Scraper (already set)
- **Description**: Verify it matches your README
- **Category**: Select appropriate category (e.g., "Data Extraction", "Social Media")
- **Tags**: Add relevant tags like `reddit`, `scraper`, `social-media`, `api`

### 2. Resources

Verify default resource settings:
- **Memory**: 4096 MB (default)
- **CPU Units**: 1024 (default)
- **Timeout**: 3600 seconds (1 hour, default)

Adjust if needed based on your usage patterns.

### 3. Input Schema

The input schema from `input_schema.json` should be automatically loaded. Verify:
- All fields are present
- Default values are correct
- Descriptions are clear

### 4. Test Run

Run a test to verify everything works:

1. Go to actor page in Apify Console
2. Click **"Start"** button
3. Use default input or provide test input:
   ```json
   {
     "subreddits": ["programming"],
     "sortBy": "hot",
     "limit": 5
   }
   ```
4. Monitor the run in real-time
5. Check output dataset after completion

### 5. Visibility Settings

Choose visibility:
- **Private**: Only you can see and run it
- **Public**: Visible in Apify Store (for publishing)

## Publishing to Apify Store

If you want to make your actor available in the Apify Store:

### Step 1: Prepare Store Listing

1. Go to actor settings → **"Store"** tab
2. Fill in store listing:
   - **Store Title**: Reddit Scraper
   - **Store Description**: Detailed description for users
   - **Screenshots**: Add screenshots of output data
   - **Example Output**: Provide sample dataset
   - **Use Cases**: Describe when to use this actor
   - **Pricing**: Set price per run (or make it free)

### Step 2: Review Requirements

Ensure your actor meets store requirements:
- ✅ Clear documentation (README.md)
- ✅ Working input schema
- ✅ Example outputs
- ✅ Error handling
- ✅ Respects rate limits

### Step 3: Submit for Review

1. Click **"Publish to Store"**
2. Review all information
3. Submit for Apify team review
4. Wait for approval (usually 1-3 business days)

## Version Management

### Creating New Versions

```bash
# Update version in actor.json
# Then push:
apify push

# Or use semantic versioning:
# Update version in .actor/actor.json manually
# Then push
```

### Tagging Releases

```bash
# Create a git tag
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# This will trigger CD workflow and create a new actor version
```

## Monitoring and Maintenance

### View Runs

1. Go to actor page
2. Click **"Runs"** tab
3. View all past runs with:
   - Status (succeeded/failed)
   - Duration
   - Resource usage
   - Output dataset

### View Logs

1. Open a specific run
2. Click **"Log"** tab
3. View real-time logs (for active runs) or historical logs

### Monitor Metrics

- **Success Rate**: Percentage of successful runs
- **Average Duration**: How long runs take
- **Resource Usage**: Memory and CPU usage
- **Error Rate**: Frequency of errors

## Troubleshooting

### Issue: `apify push` fails with version error

**Error:** `Version number must be MAJOR.MINOR, where MAJOR and MINOR is a number in range from 0 to 99.`

**Solution:**
- Change version in `.actor/actor.json` from `1.0.0` to `1.0`
- Apify requires `MAJOR.MINOR` format, not semantic versioning

### Issue: `apify push` fails with storage error

**Error:** `File ".actor/storage/key_value_stores/default" does not exist!`

**Solution:**
- Remove the `storages` section from `.actor/actor.json`
- Apify manages storage automatically - you don't need to specify storage paths

### Issue: `apify push` fails

**Solutions:**
- Verify you're logged in: `apify login`
- Check actor.json syntax is valid (use JSON validator)
- Ensure Dockerfile is correct
- Review error messages in terminal
- Verify entrypoint file exists and matches actor.json

### Issue: Actor fails to start

**Solutions:**
- Check logs in Apify Console
- Verify entrypoint in actor.json matches your main file
- Ensure all dependencies are in requirements.txt
- Test locally first: `apify run`

### Issue: Build timeout

**Solutions:**
- Optimize Dockerfile
- Reduce dependencies if possible
- Check Apify build logs for specific errors

### Issue: Runtime errors

**Solutions:**
- Review run logs in Apify Console
- Test with same input locally
- Check for missing environment variables
- Verify API endpoints are accessible

## Best Practices

1. **Test Locally First**: Always test with `apify run` before pushing
2. **Version Control**: Use semantic versioning for releases
3. **Documentation**: Keep README.md updated
4. **Monitoring**: Regularly check run success rates
5. **Error Handling**: Implement proper error handling and logging
6. **Rate Limiting**: Respect API rate limits
7. **Resource Optimization**: Monitor and optimize memory/CPU usage

## Deployment Status

✅ **Successfully Deployed!**

- **Actor Name**: `reddit-scraper`
- **Actor ID**: `gSvWJyP9OAi3h0zD0`
- **Version**: `1.0`
- **Status**: Deployed and ready to use
- **Console URL**: https://console.apify.com/organization/uHl0TkYbhB3y3Ex0o/actors/gSvWJyP9OAi3h0zD0

## Deployment Experience & Lessons Learned

### Initial Deployment Issues

During the first deployment attempt, we encountered two issues that are now documented:

1. **Version Format Error**
   - **Issue**: Apify requires version format `MAJOR.MINOR` (e.g., `1.0`), not semantic versioning `MAJOR.MINOR.PATCH` (e.g., `1.0.0`)
   - **Fix**: Changed version in `.actor/actor.json` from `1.0.0` to `1.0`
   - **Lesson**: Always check Apify's version format requirements before deployment

2. **Storage Path Error**
   - **Issue**: Build failed with error about missing storage directories
   - **Fix**: Removed the `storages` section from `actor.json` - Apify manages storage automatically
   - **Lesson**: Apify handles storage internally; don't specify storage paths in actor.json

### Successful Deployment Process

1. ✅ Verified Apify CLI installation and login
2. ✅ Fixed version format in `actor.json`
3. ✅ Removed `storages` section from `actor.json`
4. ✅ Ran `apify push` successfully
5. ✅ Build completed on Apify's servers
6. ✅ Actor created and ready to use

### Key Takeaways

- **Version Format**: Use `MAJOR.MINOR` format (0-99 for each)
- **Storage**: Let Apify manage storage automatically
- **Build Process**: Apify builds Docker images on their servers (no need to push pre-built images)
- **First Push**: Creates a new actor; subsequent pushes update the existing actor

## Next Steps

After successful deployment:

1. ✅ **Deployed to Apify** - Actor is live and ready
2. 🔄 Run test executions in Apify Console
3. 🔄 Monitor performance and logs
4. 🔄 Configure actor settings (tags, categories, visibility)
5. 🔄 Gather user feedback (if published)
6. 🔄 Iterate and improve
7. 🔄 Consider publishing to store

## Additional Resources

- [Apify Documentation](https://docs.apify.com)
- [Apify CLI Reference](https://docs.apify.com/cli)
- [Apify Store Guidelines](https://docs.apify.com/store/guidelines)
- [Apify API Reference](https://docs.apify.com/api/v2)

---

**Last Updated**: December 2024
**Version**: 1.0
**Deployment Status**: ✅ Successfully Deployed

