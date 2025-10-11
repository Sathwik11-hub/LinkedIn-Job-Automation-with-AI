# Contributing to AutoAgentHire

Thank you for considering contributing to AutoAgentHire! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case** for the enhancement
- **Proposed solution** or implementation
- **Alternative solutions** considered
- **Potential drawbacks** or concerns

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** outlined below
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure tests pass** before submitting
6. **Write clear commit messages**

#### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions/updates

#### Commit Message Format

```
type: Short description (50 chars or less)

Detailed explanation if needed (wrap at 72 chars).

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autoagenthire.git
   cd autoagenthire
   ```

2. **Run setup script**
   ```bash
   ./setup.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install black pylint pytest pytest-asyncio pytest-cov
   ```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Quotes**: Double quotes for strings
- **Imports**: Organized with isort
- **Formatting**: Use Black formatter
- **Type hints**: Required for function signatures
- **Docstrings**: Google style docstrings

#### Example

```python
"""
Module docstring describing the module purpose.
"""
from typing import List, Dict, Any


def calculate_match_score(
    resume_data: Dict[str, Any],
    job_requirements: List[str]
) -> float:
    """
    Calculate job match score based on resume and requirements.
    
    Args:
        resume_data: Parsed resume information
        job_requirements: List of job requirements
        
    Returns:
        Match score between 0 and 100
        
    Raises:
        ValueError: If resume_data is invalid
    """
    # Implementation
    pass
```

### Code Quality Tools

Run these before submitting:

```bash
# Format code
black backend/

# Check linting
pylint backend/

# Run type checking
mypy backend/

# Run tests
pytest tests/
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

This will automatically:
- Format code with Black
- Check linting with Flake8
- Run type checking with mypy
- Check for security issues with bandit

## Testing Guidelines

### Writing Tests

- Use **pytest** for all tests
- Place tests in appropriate directories:
  - `tests/unit/` - Unit tests
  - `tests/integration/` - Integration tests
  - `tests/e2e/` - End-to-end tests
- Use **fixtures** for common setup
- Use **mocking** for external services
- Aim for **>80% code coverage**

#### Test Example

```python
import pytest
from backend.agents.job_search_agent import JobSearchAgent


@pytest.fixture
def agent():
    return JobSearchAgent()


@pytest.mark.asyncio
async def test_search_jobs(agent):
    """Test job search returns results."""
    results = await agent.search_jobs(
        keywords="Python Developer",
        location="San Francisco"
    )
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_agents.py

# With coverage
pytest --cov=backend tests/

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Documentation

### Code Documentation

- All public functions/classes must have docstrings
- Use Google-style docstrings
- Include usage examples for complex functions
- Update API documentation when adding endpoints

### Documentation Files

When updating documentation:

- `README.md` - Project overview and quick start
- `docs/API.md` - API endpoint documentation
- `docs/ARCHITECTURE.md` - System architecture
- `docs/DEPLOYMENT.md` - Deployment instructions
- `docs/USER_GUIDE.md` - User guide

## Project Structure

Understand the project structure:

```
autoagenthire/
├── backend/          # Backend application
│   ├── agents/       # AI agents
│   ├── api/          # API routes
│   ├── automation/   # Web automation
│   ├── database/     # Database models
│   ├── llm/          # LLM integration
│   └── ...
├── frontend/         # Frontend applications
├── tests/           # Test suite
├── docs/            # Documentation
└── scripts/         # Utility scripts
```

## Release Process

1. Update version in `backend/__init__.py`
2. Update CHANGELOG.md
3. Create release branch: `release/v1.x.x`
4. Run full test suite
5. Update documentation
6. Create GitHub release
7. Deploy to production

## Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: support@autoagenthire.com

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Annual contributor showcase

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AutoAgentHire! 🚀
