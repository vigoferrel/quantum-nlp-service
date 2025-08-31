# Contributing to Quantum NLP Service

Thank you for your interest in contributing to Quantum NLP Service! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** and **Push** your changes
7. **Create** a Pull Request

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- OpenRouter API key (for testing)
- Basic knowledge of LLM optimization

## 🛠️ Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vigoferrel/quantum-nlp-service.git
cd quantum-nlp-service
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run Tests

```bash
python -m pytest tests/ -v
```

## 📝 Code Style Guidelines

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Docstrings**: Google style
- **Type Hints**: Required for all functions

### Example Code Structure

```python
from typing import Dict, Any, Optional
import asyncio


class QuantumOptimizer:
    """Quantum optimization engine for LLM performance enhancement.
    
    This class implements advanced quantum-based optimization strategies
    for improving LLM performance across multiple domains.
    
    Attributes:
        api_key (str): OpenRouter API key
        model (str): Target model for optimization
        strategies (Dict): Available optimization strategies
    """
    
    def __init__(self, api_key: str, model: str = "google/gemini-flash-1.5-8b"):
        """Initialize the quantum optimizer.
        
        Args:
            api_key: OpenRouter API key for model access
            model: Target model for optimization
            
        Raises:
            ValueError: If API key is invalid
        """
        self.api_key = api_key
        self.model = model
        self.strategies = self._initialize_strategies()
    
    async def optimize_domain(self, domain: str, query: str) -> Dict[str, Any]:
        """Optimize performance for a specific domain.
        
        Args:
            domain: Target domain (reasoning, mathematics, programming, etc.)
            query: Test query for optimization
            
        Returns:
            Dictionary containing optimization results
            
        Raises:
            OptimizationError: If optimization fails
        """
        # Implementation here
        pass
```

## 🧪 Testing Guidelines

### Writing Tests

1. **Test Structure**: Use pytest
2. **Test Naming**: `test_<function_name>_<scenario>`
3. **Coverage**: Aim for 90%+ coverage
4. **Mocking**: Mock external API calls

### Example Test

```python
import pytest
from unittest.mock import Mock, patch
from quantum_optimization_engine import QuantumOptimizer


class TestQuantumOptimizer:
    """Test cases for QuantumOptimizer class."""
    
    @pytest.fixture
    def optimizer(self):
        """Create optimizer instance for testing."""
        return QuantumOptimizer("test_api_key")
    
    @pytest.mark.asyncio
    async def test_optimize_domain_success(self, optimizer):
        """Test successful domain optimization."""
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json.return_value = {
                'choices': [{'message': {'content': 'Test response'}}]
            }
            mock_post.return_value.__aenter__.return_value = mock_response
            
            result = await optimizer.optimize_domain('reasoning', 'Test query')
            
            assert result['success'] is True
            assert 'score' in result
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_quantum_optimizer.py

# Run with verbose output
pytest -v
```

## 🔧 Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/quantum-enhancement

# Make changes
# ... edit files ...

# Add changes
git add .

# Commit with conventional commit message
git commit -m "feat: add quantum superposition optimization"

# Push to your fork
git push origin feature/quantum-enhancement
```

### 2. Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Examples:**
```
feat(optimization): add quantum entanglement strategy
fix(evaluation): resolve scoring calculation error
docs(readme): update installation instructions
test(quantum): add comprehensive test suite
```

### 3. Pull Request Process

1. **Title**: Clear, descriptive title
2. **Description**: Detailed description of changes
3. **Tests**: Include test coverage
4. **Documentation**: Update relevant docs
5. **Review**: Address reviewer feedback

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🐛 Bug Reports

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9.0]
- Package Version: [e.g., 1.0.0]

**Additional Information**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why this feature is needed

**Proposed Implementation**
How you think it should be implemented

**Alternatives Considered**
Other approaches you considered

**Additional Information**
Any other relevant information
```

## 🔒 Security

### Security Guidelines

1. **API Keys**: Never commit API keys or sensitive data
2. **Dependencies**: Keep dependencies updated
3. **Input Validation**: Validate all user inputs
4. **Error Handling**: Don't expose sensitive information in errors

### Reporting Security Issues

For security issues, please email: vigoferrel@gmail.com

## 📚 Documentation

### Documentation Guidelines

1. **Docstrings**: Use Google style docstrings
2. **README**: Keep README updated
3. **Examples**: Include usage examples
4. **API Docs**: Document all public APIs

### Example Docstring

```python
def quantum_optimize(
    prompt: str,
    strategy: str = "hybrid_enhanced",
    domain: Optional[str] = None
) -> Dict[str, Any]:
    """Apply quantum optimization to a prompt.
    
    This function applies advanced quantum optimization strategies
    to improve LLM performance for specific domains.
    
    Args:
        prompt: The input prompt to optimize
        strategy: Optimization strategy to use
        domain: Target domain for optimization
        
    Returns:
        Dictionary containing:
            - optimized_prompt: The optimized prompt
            - score: Performance score
            - strategy_used: Strategy applied
            
    Raises:
        ValueError: If strategy is invalid
        OptimizationError: If optimization fails
        
    Example:
        >>> result = quantum_optimize("Solve this math problem", "mathematics")
        >>> print(result['optimized_prompt'])
        "Implementa con notación matemática formal: Solve this math problem"
    """
```

## 🤝 Community Guidelines

### Code of Conduct

1. **Be Respectful**: Treat others with respect
2. **Be Helpful**: Help others learn and grow
3. **Be Constructive**: Provide constructive feedback
4. **Be Inclusive**: Welcome diverse perspectives

### Communication

- **Issues**: Use GitHub issues for bugs and features
- **Discussions**: Use GitHub discussions for questions
- **Email**: vigoferrel@gmail.com for private matters

## 🏆 Recognition

### Contributors

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

### Contribution Levels

- **Bronze**: 1-5 contributions
- **Silver**: 6-15 contributions
- **Gold**: 16+ contributions
- **Platinum**: Major feature contributions

## 📞 Contact

For questions about contributing:
- **Email**: vigoferrel@gmail.com
- **GitHub Issues**: Use GitHub issues for technical questions
- **Discussions**: Use GitHub discussions for general questions

---

Thank you for contributing to Quantum NLP Service! 🚀
