# Contribution Guidelines

## Welcome Contributors! 👋

Thank you for your interest in contributing to AI Humanizer. This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Report issues professionally
- Give credit where credit is due

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/ai-humanizer.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up development environment (see README.md)

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_app.py -v

# Start development server
python app.py
```

## Making Changes

### Code Style
- Follow PEP 8
- Use type hints
- Write descriptive docstrings
- Keep functions focused and small

### Commit Messages
- Use clear, descriptive messages
- Start with a verb (feat:, fix:, docs:, chore:, etc.)
- Example: `feat: Add batch processing endpoint`

### Testing
- Write tests for new features
- Ensure all tests pass: `pytest test_app.py -v`
- Aim for good test coverage

### Documentation
- Update README.md if adding features
- Add docstrings to functions
- Include examples for new endpoints

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Create clear PR title and description
4. Reference any related issues
5. Request review from maintainers
6. Address feedback promptly

## Feature Request

- Use GitHub Issues with `enhancement` label
- Provide clear use case
- Include examples if applicable
- Be open to discussion

## Bug Reports

- Use GitHub Issues with `bug` label
- Include minimal reproducible example
- Specify Python version and OS
- Provide error logs/tracebacks

## Questions or Help

- Check existing issues/discussions first
- Ask in GitHub Discussions
- Be patient and respectful

## Supported Versions

- Python 3.8+
- FastAPI 0.104+
- Recent Ollama versions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making AI Humanizer better! 🙏
