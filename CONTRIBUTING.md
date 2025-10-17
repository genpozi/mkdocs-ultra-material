# Contributing to MkDocs Ultra Material

Thank you for your interest in contributing to MkDocs Ultra Material! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling, insulting, or derogatory remarks
- Personal or political attacks
- Publishing others' private information
- Any conduct that could be considered inappropriate in a professional setting

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of MkDocs
- Familiarity with AI/LLM concepts (helpful but not required)

### Finding Issues to Work On

1. Check the [issue tracker](https://github.com/genpozi/mkdocs-ultra-material/issues)
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to let others know you're working on it
4. Ask questions if anything is unclear

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/mkdocs-ultra-material.git
cd mkdocs-ultra-material
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### 4. Set Up Pre-commit Hooks (Optional)

```bash
pre-commit install
```

### 5. Configure API Keys for Testing

```bash
export OPENROUTER_API_KEY="your-test-api-key"
# or create .env file
echo "OPENROUTER_API_KEY=your-test-api-key" > .env
```

---

## How to Contribute

### Types of Contributions

#### 🐛 Bug Reports

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Error messages or logs

#### ✨ Feature Requests

Have an idea? Open an issue with:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if you have ideas)
- Examples of similar features elsewhere

#### 📝 Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples or use cases
- Improve existing guides
- Translate documentation

#### 🔧 Code Contributions

Ready to code? Great! Follow the process below.

---

## Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Imports**: Use absolute imports, grouped by standard library, third-party, local
- **Type hints**: Required for all public functions and methods
- **Docstrings**: Google-style docstrings for all public APIs

### Code Formatting

We use automated tools:

```bash
# Format code
black mkdocs_ai/

# Check linting
ruff check mkdocs_ai/

# Type checking
mypy mkdocs_ai/
```

### Example Code Style

```python
from typing import Optional

from mkdocs_ai.providers.base import AIProvider


class MyProvider(AIProvider):
    """Custom AI provider implementation.
    
    This provider implements the AIProvider interface for a custom
    AI service.
    
    Args:
        api_key: API key for authentication
        base_url: Base URL for the API endpoint
        
    Example:
        ```python
        provider = MyProvider(api_key="key", base_url="https://api.example.com")
        response = await provider.generate("Write a guide")
        ```
    """
    
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate text from a prompt.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific options
            
        Returns:
            Generated text response
            
        Raises:
            ProviderError: If generation fails
        """
        # Implementation here
        pass
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mkdocs_ai --cov-report=html

# Run specific test file
pytest tests/test_providers.py

# Run specific test
pytest tests/test_providers.py::test_openrouter_provider
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Include both positive and negative test cases

Example test:

```python
import pytest
from mkdocs_ai.providers.openrouter import OpenRouterProvider


@pytest.mark.asyncio
async def test_openrouter_generate():
    """Test OpenRouter provider generates text successfully."""
    provider = OpenRouterProvider(api_key="test-key")
    
    # Mock the API call
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.return_value.__aenter__.return_value.json.return_value = {
            "choices": [{"message": {"content": "Generated text"}}]
        }
        
        result = await provider.generate("Test prompt")
        
        assert result == "Generated text"
        mock_post.assert_called_once()
```

---

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.
    
    Longer description if needed. Can span multiple lines
    and include examples.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Example:
        ```python
        result = function_name("test", 42)
        print(result)  # True
        ```
    """
    pass
```

### Documentation Files

When adding new features, update:
- README.md (if user-facing)
- Relevant guide in docs/
- IMPLEMENTATION_STATUS.md
- Add examples to PRACTICAL_EXAMPLES.md

---

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Test additions or fixes

### 2. Make Your Changes

- Write clear, focused commits
- Follow coding standards
- Add tests for new features
- Update documentation

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: add new provider support

- Implement CustomProvider class
- Add tests for custom provider
- Update documentation

Closes #123"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Link to related issues
- Screenshots (if UI changes)
- Checklist of completed items

### 5. PR Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description is complete

### 6. Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged
- Your contribution will be credited

---

## Development Workflow

### Typical Workflow

1. **Pick an issue** or create one for discussion
2. **Fork and clone** the repository
3. **Create a branch** for your work
4. **Make changes** with tests and docs
5. **Run tests** and linting locally
6. **Commit** with clear messages
7. **Push** and create a pull request
8. **Respond** to review feedback
9. **Celebrate** when merged! 🎉

### Working with AI Providers

When adding or modifying AI providers:

1. Implement the `AIProvider` interface
2. Add provider configuration to `config.py`
3. Add tests with mocked API calls
4. Update provider documentation
5. Add example usage

### Adding New Features

For new features:

1. Discuss in an issue first
2. Update IMPLEMENTATION_STATUS.md
3. Create feature branch
4. Implement with tests
5. Update all relevant documentation
6. Submit PR with examples

---

## Getting Help

### Questions?

- **GitHub Discussions**: For general questions and ideas
- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check existing docs first

### Stuck?

Don't hesitate to ask for help! We're here to support you:
- Comment on the issue you're working on
- Ask in GitHub Discussions
- Tag maintainers in your PR

---

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- CONTRIBUTORS.md file (coming soon)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You!

Your contributions make MkDocs Ultra Material better for everyone. We appreciate your time and effort! 🙏

---

**Questions?** Open an issue or start a discussion. We're happy to help!
