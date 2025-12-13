# Code Formatting and Quality Standards

This document outlines the code formatting and quality standards enforced in this project.

## ⚠️ Pre-Push Checklist (REQUIRED)

**IMPORTANT:** Always run these commands before pushing code to avoid CI failures:

```bash
# 1. Format code with Black (run first)
black src/ tests/

# 2. Sort imports with isort (configured for Black compatibility)
isort src/ tests/

# 3. Verify formatting (must pass before pushing)
black --check src/ tests/
isort --check-only src/ tests/

# 4. Run tests
pytest tests/ -v
```

**The CI pipeline will fail if these checks don't pass!** Never skip this step.

## Code Formatters

The project uses automated code formatting tools to maintain consistent code style across the codebase.

### Black

[Black](https://black.readthedocs.io/) is the primary code formatter for Python code. It automatically formats code according to PEP 8 style guidelines.

**Usage:**

```bash
# Format all code
black src/ tests/

# Check formatting without making changes
black --check src/ tests/
```

**Configuration:**
- Black uses default settings (line length: 88 characters)
- All Python files in `src/` and `tests/` are formatted
- CI/CD pipeline enforces Black formatting on every push

**Before Committing:**
Always run Black before committing code:

```bash
black src/ tests/
```

### isort

[isort](https://pycqa.github.io/isort/) automatically sorts and organizes import statements.

**Usage:**

```bash
# Sort imports
isort src/ tests/

# Check import sorting without making changes
isort --check-only src/ tests/
```

**Configuration:**
- Configured in `pyproject.toml` to use Black's profile for compatibility
- CI/CD pipeline enforces import sorting on every push
- Automatically compatible with Black formatting

## Linting

### flake8

[flake8](https://flake8.pycqa.org/) performs static analysis to find bugs and style issues.

**Usage:**

```bash
# Run flake8
flake8 src/ tests/
```

**Configuration:**
- Maximum line length: 127 characters
- Maximum complexity: 10
- Runs in CI/CD pipeline on every push

**Error Codes:**
- `E9`: Runtime errors (indentation, syntax)
- `F63`: Syntax errors in print statements
- `F7`: Syntax errors in function definitions
- `F82`: Undefined names

## Type Checking

### mypy

[mypy](https://mypy.readthedocs.io/) performs static type checking (optional, not enforced in CI).

**Usage:**

```bash
# Type check code
mypy src/
```

## Pre-commit Checklist

Before committing and pushing code, ensure:

1. ✅ **Format code with Black:**
   ```bash
   black src/ tests/
   ```

2. ✅ **Sort imports with isort:**
   ```bash
   isort src/ tests/
   ```

3. ✅ **Verify formatting (CRITICAL - CI will fail if this doesn't pass):**
   ```bash
   black --check src/ tests/
   isort --check-only src/ tests/
   ```

4. ✅ **Run linting:**
   ```bash
   flake8 src/ tests/
   ```

5. ✅ **Run tests:**
   ```bash
   pytest tests/ -v
   ```

**Remember:** The CI pipeline runs `black --check` and `isort --check-only`. If these fail locally, they will fail in CI too!

## CI/CD Enforcement

The CI/CD pipeline automatically checks:

- ✅ Code formatting (Black)
- ✅ Import sorting (isort)
- ✅ Code quality (flake8)
- ✅ Test coverage (pytest)

**If CI fails:**
1. Check the error message in GitHub Actions
2. Run the failing command locally
3. Fix the issues
4. Commit and push again

## Development Dependencies

To install all development tools:

```bash
pip install black isort flake8 mypy
```

Or add to your local development environment:

```bash
pip install -r requirements.txt
pip install black isort flake8 mypy
```

## IDE Integration

### VS Code

Install the Black Formatter extension:
- Extension ID: `ms-python.black-formatter`
- Enable format on save in settings

### PyCharm

1. Go to Settings → Tools → External Tools
2. Add Black as an external tool
3. Configure to run on file save

## Code Style Guidelines

### General

- Follow PEP 8 style guide
- Use Black for automatic formatting
- Keep functions focused and small
- Use type hints where appropriate
- Write descriptive docstrings

### Naming Conventions

- **Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** Prefix with `_` (single underscore)

### Line Length

- Maximum: 88 characters (Black default)
- Can be up to 127 characters for flake8 warnings

### Imports

- Use isort to automatically organize imports
- Group imports: standard library, third-party, local
- Use absolute imports when possible

## Examples

### Before Black Formatting

```python
def   scrape_posts(  subreddit:str,limit:int=25)->List[Dict]:
    posts=[]
    # ... code ...
    return posts
```

### After Black Formatting

```python
def scrape_posts(subreddit: str, limit: int = 25) -> List[Dict]:
    posts = []
    # ... code ...
    return posts
```

## Troubleshooting

**Black not formatting correctly?**
- Ensure Black is installed: `pip install black`
- Check file extensions are `.py`
- Verify Black version: `black --version`

**isort conflicts with Black?**
- isort is configured in `pyproject.toml` to use Black's profile automatically
- Always run Black first, then isort
- If issues persist, ensure `pyproject.toml` has `[tool.isort] profile = "black"`

**flake8 errors after Black?**
- Some flake8 rules may conflict with Black
- Use `# noqa` comments for specific lines if needed
- Adjust flake8 configuration if necessary

## Additional Resources

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [PEP 8 Style Guide](https://pep8.org/)

