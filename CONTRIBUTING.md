# Contributing to AutoAgentHire

Thank you for your interest in contributing to AutoAgentHire! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/LinkedIn-Job-Automation-with-AI.git`
3. Add upstream remote: `git remote add upstream https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI.git`

## Development Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for React frontend)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
make install-dev
# or
pip install -r requirements.txt
pip install -e ".[dev]"
```

3. Setup environment:
```bash
make setup
# Edit .env file with your configuration
```

4. Initialize database:
```bash
make db-upgrade
```

## Making Changes

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring
- `test/description` - Test additions/modifications

### Development Workflow

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes

3. Run quality checks:
```bash
make quality
```

4. Run tests:
```bash
make test
```

5. Commit your changes (see [Commit Messages](#commit-messages))

6. Push to your fork:
```bash
git push origin feature/your-feature-name
```

7. Create a Pull Request

## Testing

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests
make test-integration

# E2E tests
make test-e2e

# With coverage
make test-cov
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Place E2E tests in `tests/e2e/`
- Use descriptive test names: `test_should_create_job_application_when_valid_data()`
- Follow AAA pattern: Arrange, Act, Assert
- Use fixtures defined in `conftest.py`

Example:
```python
def test_should_match_jobs_with_resume(mock_resume, mock_jobs):
    # Arrange
    matcher = JobMatcher()
    
    # Act
    matches = matcher.match(mock_resume, mock_jobs)
    
    # Assert
    assert len(matches) > 0
    assert matches[0].score > 0.7
```

## Code Style

We follow PEP 8 with some modifications. Code style is enforced with:

- **Black**: Code formatter (line length: 100)
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Format Code

```bash
# Format code
make format

# Check formatting
make format-check

# Run linter
make lint

# Type checking
make type-check
```

### Style Guidelines

- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused (< 50 lines)
- Use meaningful variable names
- Avoid magic numbers; use constants

Example:
```python
from typing import List, Optional

def calculate_match_score(
    resume_skills: List[str],
    job_requirements: List[str],
    weight: float = 0.8
) -> float:
    """Calculate job match score based on skills overlap.
    
    Args:
        resume_skills: List of skills from candidate's resume
        job_requirements: List of required skills from job posting
        weight: Weight factor for scoring (default: 0.8)
        
    Returns:
        Match score between 0.0 and 1.0
    """
    # Implementation
    pass
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Examples

```
feat(agents): add job search agent with LinkedIn integration

fix(api): handle timeout errors in job application endpoint

docs(readme): update installation instructions

test(matching): add unit tests for job matching algorithm
```

## Pull Request Process

1. **Update Documentation**: Update README, docstrings, and comments as needed

2. **Add Tests**: Ensure new code has adequate test coverage

3. **Run Quality Checks**: 
   ```bash
   make ci
   ```

4. **Update CHANGELOG**: Add entry describing your changes

5. **Fill PR Template**: Provide clear description of changes

6. **Request Review**: Assign reviewers and wait for approval

7. **Address Feedback**: Make requested changes and push updates

8. **Squash Commits** (if requested): Clean up commit history before merge

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Security considerations addressed
- [ ] Performance impact considered
- [ ] Backward compatibility maintained

## Reporting Bugs

### Before Submitting

- Check existing issues
- Verify it's not already fixed in latest version
- Collect relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- Package version: [e.g., 0.1.0]

**Additional Context**
Logs, screenshots, etc.
```

## Suggesting Enhancements

### Feature Request Template

```markdown
**Problem Statement**
Clear description of the problem or limitation

**Proposed Solution**
Detailed description of proposed enhancement

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Use cases, examples, mockups, etc.
```

## Security

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email security concerns to: [security contact]
3. Provide detailed description and reproduction steps
4. Allow time for fix before public disclosure

## Questions?

- Open a [Discussion](https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI/discussions)
- Join our community chat
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AutoAgentHire! 🚀
