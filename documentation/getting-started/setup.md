# Setup Guide for Reddit Scraper Actor

## Prerequisites

### 1. Install Python Dependencies

```bash
cd reddit-scraper-actor
pip install -r requirements.txt
```

This will install:
- `apify` - Apify Python SDK
- `aiohttp` - Async HTTP client for Reddit API

### 2. Install Apify CLI (Optional, for local testing)

The Apify CLI is used for local testing and deployment. It requires Node.js:

```bash
# Check if Node.js is installed
node --version
npm --version

# If not installed, download from https://nodejs.org/

# Install Apify CLI globally
npm install -g apify-cli

# Login to Apify
apify login

# Verify installation
apify info
```

## Local Testing (Without Apify CLI)

You can test the actor locally without the Apify CLI using the provided test runner:

```bash
# Run with default test-input.json
python3 run_local.py

# Or specify a different input file
python3 run_local.py test-input.json
```

The `run_local.py` script will:
- Read the input from the JSON file
- Set up the local storage directory
- Run the actor with the provided input
- Handle errors gracefully

**Alternative: Direct Python execution**

If you prefer to run directly without the test runner:

```bash
# Set up storage directory
export APIFY_LOCAL_STORAGE_DIR=./storage
mkdir -p storage/key_value_stores/default

# Write input to the file that Actor.get_input() reads from
echo '{"subreddits": ["programming"], "sortBy": "hot", "limit": 5}' > storage/key_value_stores/default/INPUT.json

# Run the actor (use root main.py, not src/main.py)
python3 main.py
```

**Note**: 
- The `run_local.py` script handles all of this automatically, so it's the recommended method
- Always use `main.py` (root) as the entrypoint, not `src/main.py`
- The root `main.py` manages the Actor context and calls the scraper logic from `src/main.py`

## Testing with Apify CLI

Once Apify CLI is installed:

```bash
# Create a test input file
cat > test-input.json << EOF
{
  "subreddits": ["programming"],
  "sortBy": "hot",
  "limit": 5
}
EOF

# Run the actor with test input
# Note: Use --input-file (not -t) for specifying input file
apify run --input-file test-input.json
```

**Important**: The project includes a `package.json` file as a workaround for Apify CLI v1.1.1's limitation with detecting Python actors. This allows the CLI to properly run the actor by executing `python3 main.py`.

## Deployment

```bash
# Push to Apify platform
apify push
```

## Project Structure

Understanding the project structure is crucial for troubleshooting:

```
reddit-scraper-actor/
├── main.py                 # Root entrypoint (uses Actor context manager)
├── src/
│   └── main.py            # Core scraper logic (run_scraper function)
├── package.json           # Workaround for CLI detection (runs python3 main.py)
├── .actor/
│   └── actor.json         # Actor configuration (entrypoint: main.py)
├── Dockerfile             # Container configuration
└── run_local.py           # Local test runner
```

**Key Points:**
- `main.py` (root) is the entrypoint that uses the Actor context manager directly
- `src/main.py` contains the `run_scraper()` function that performs the actual scraping
- The Actor context manager is only used in the root `main.py`, not in `src/main.py`
- `package.json` is required for Apify CLI v1.1.1 to detect and run the Python actor

## Troubleshooting

### Issue: `apify` command not found
**Symptoms:**
```
bash: apify: command not found
```

**Solution:**
1. Install Node.js from https://nodejs.org/ (required for Apify CLI)
2. Install Apify CLI globally:
   ```bash
   npm install -g apify-cli
   ```
3. Verify installation:
   ```bash
   apify --version
   apify info
   ```

### Issue: `apify-sdk` package not found
**Symptoms:**
```
ModuleNotFoundError: No module named 'apify-sdk'
```

**Solution:**
- The correct package name is `apify` (not `apify-sdk`)
- Install the correct package:
  ```bash
  pip install apify aiohttp
  ```
- Or install from requirements:
  ```bash
  pip install -r requirements.txt
  ```

### Issue: Import errors when running locally
**Symptoms:**
```
ModuleNotFoundError: No module named 'src'
ImportError: cannot import name 'run_scraper' from 'src.main'
```

**Solutions:**
1. Make sure you're in the `reddit-scraper-actor` directory:
   ```bash
   cd reddit-scraper-actor
   ```
2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Verify Python can find the modules:
   ```bash
   python3 -c "from src.main import run_scraper; print('Import successful')"
   ```
4. If using `run_local.py`, make sure it imports from `main` (root), not `src.main`:
   ```python
   from main import main as actor_main  # Correct
   # NOT: from src.main import main as actor_main
   ```

### Issue: "Actor is of an unknown format" error
**Symptoms:**
```
Error: Actor is of an unknown format. Make sure your project is supported by Apify CLI 
(either a package.json file is present, or a Python entrypoint could be found) 
or you are in a migrated Scrapy project.
```

**Root Cause:**
- Apify CLI v1.1.1 has a known limitation detecting Python actors, especially when the entrypoint is in a subdirectory
- The CLI looks for either a `package.json` file or a Python entrypoint it can detect

**Solution (Already Implemented):**
The project includes a `package.json` file that tells the CLI to run `python3 main.py`. This is a workaround that allows the CLI to properly detect and run the actor.

**If you still encounter this error:**
1. Verify `package.json` exists and contains:
   ```json
   {
     "scripts": {
       "start": "python3 main.py"
     }
   }
   ```
2. Verify `main.py` exists at the root level and imports `apify`:
   ```python
   from apify import Actor
   ```
3. Try running directly with Python to verify the actor works:
   ```bash
   python3 run_local.py test-input.json
   ```
4. As a last resort, use the local test runner instead:
   ```bash
   python3 run_local.py test-input.json
   ```

**Note**: This CLI detection issue doesn't affect deployment to the Apify platform - `apify push` should work fine regardless.

### Issue: "python: command not found" when using Apify CLI
**Symptoms:**
```
sh: python: command not found
Error: npm exited with code 127
```

**Solution:**
- Update `package.json` to use `python3` instead of `python`:
  ```json
  {
    "scripts": {
      "start": "python3 main.py"
    }
  }
  ```
- On macOS and Linux, `python3` is typically available, while `python` may not be

### Issue: Double Actor context manager error
**Symptoms:**
```
RuntimeError: Actor context manager already in use
```

**Root Cause:**
- The Actor context manager (`async with Actor:`) should only be used once
- If both `main.py` and `src/main.py` use the context manager, this error occurs

**Solution:**
- The project structure is already correct:
  - `main.py` (root) uses `async with Actor:`
  - `src/main.py` exports `run_scraper()` which does NOT use the context manager
- If you modify the code, ensure only one file uses the Actor context manager

### Issue: Indentation errors after refactoring
**Symptoms:**
```
IndentationError: unexpected indent
```

**Solution:**
- When refactoring `src/main.py`, ensure all code inside `run_scraper()` is properly indented
- The function should start at the module level (no extra indentation)
- Use a code formatter or IDE to fix indentation:
  ```bash
   autopep8 --in-place --aggressive src/main.py
   ```

### Issue: Storage directory not found
**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: './storage/...'
```

**Solution:**
1. The `run_local.py` script automatically creates the storage directory
2. If running directly, create it manually:
   ```bash
   mkdir -p storage/key_value_stores/default
   mkdir -p storage/datasets/default
   ```
3. Or set the environment variable:
   ```bash
   export APIFY_LOCAL_STORAGE_DIR=./storage
   ```

### Issue: Input file not found
**Symptoms:**
```
Error: Input file 'test-input.json' not found.
```

**Solution:**
1. Create the input file:
   ```bash
   cat > test-input.json << EOF
   {
     "subreddits": ["programming"],
     "sortBy": "hot",
     "limit": 5
   }
   EOF
   ```
2. Or specify a different file:
   ```bash
   python3 run_local.py path/to/your-input.json
   ```

## Crucial Points to Remember

### 1. Entrypoint Structure
- **Root `main.py`** must use the Actor context manager (`async with Actor:`)
- **`src/main.py`** should export functions that DON'T use the Actor context manager
- This separation allows the CLI to detect the Python actor while keeping code organized

### 2. Package.json Requirement
- **Required for Apify CLI v1.1.1**: The `package.json` file is necessary for the CLI to detect and run the actor
- **Don't delete it**: Even though this is a Python project, the `package.json` serves as a workaround for CLI detection
- **Script must use `python3`**: Use `python3` not `python` in the start script

### 3. Actor Context Manager
- **Use only once**: The `async with Actor:` context manager should only be used in one place (root `main.py`)
- **All Actor API calls**: `Actor.get_input()`, `Actor.push_data()`, `Actor.log`, etc. must be inside the context manager
- **Function parameters**: Pass data (like `input_data`) to functions instead of calling `Actor.get_input()` multiple times

### 4. Local Testing
- **Preferred method**: Use `run_local.py` for local testing - it handles storage setup automatically
- **Direct execution**: You can run `python3 main.py` directly, but you need to set up storage first
- **CLI testing**: Use `apify run --input-file test-input.json` once everything is set up

### 5. Deployment
- **CLI detection issue doesn't affect deployment**: `apify push` works regardless of CLI detection issues
- **Dockerfile uses `main.py`**: The Dockerfile runs `python main.py`, matching the entrypoint configuration
- **Actor.json configuration**: The `.actor/actor.json` file specifies `main.py` as the entrypoint

### 6. Code Organization
- **Business logic in `src/`**: Keep the core scraping logic in `src/main.py`
- **Entrypoint at root**: Keep the Actor context manager setup in root `main.py`
- **Separation of concerns**: This structure makes testing and maintenance easier

### 7. Common Mistakes to Avoid
- ❌ Don't use `async with Actor:` in both `main.py` and `src/main.py`
- ❌ Don't delete `package.json` thinking it's not needed for Python projects
- ❌ Don't use `python` instead of `python3` in `package.json`
- ❌ Don't change the entrypoint in `.actor/actor.json` without updating `Dockerfile`
- ❌ Don't call `Actor.get_input()` inside `run_scraper()` - pass it as a parameter instead

### 8. Verification Checklist
Before deploying or sharing your actor, verify:
- [ ] `package.json` exists and uses `python3 main.py`
- [ ] `main.py` (root) imports and uses `Actor` context manager
- [ ] `src/main.py` exports `run_scraper()` function (no Actor context)
- [ ] `.actor/actor.json` specifies `main.py` as entrypoint
- [ ] `Dockerfile` runs `python main.py`
- [ ] `run_local.py` imports from `main` (not `src.main`)
- [ ] Local testing works: `python3 run_local.py test-input.json`
- [ ] CLI testing works: `apify run --input-file test-input.json`

