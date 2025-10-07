# Contributing to EWU Course Fetching Tool

First off, thank you for considering contributing to the EWU Course Fetching Tool! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed feature**
- **Explain why this enhancement would be useful**
- **List any similar features in other tools**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the code style** - Use PEP 8 for Python code
3. **Test your changes** - Ensure everything works as expected
4. **Update documentation** - Update README.md if you change functionality
5. **Write clear commit messages**
6. **Submit your pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ewu-course-tool.git
cd ewu-course-tool/tool

# Install dependencies
pip install -r requirements.txt

# Run the tool
python main.py
```

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to all functions and classes

### Example Function

```python
def fetch_courses(session_id: str) -> dict:
    """
    Fetch course data from EWU portal
    
    Args:
        session_id: Active session ID from authentication
        
    Returns:
        Dictionary containing status and courses list
        
    Raises:
        ConnectionError: If unable to connect to portal
    """
    # Implementation here
    pass
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests after the first line

**Examples:**
```
Add CSV export functionality

- Implement CSV export module
- Add export option to main menu
- Update README with CSV documentation
Fixes #123
```

## Project Structure

```
tool/
├── main.py              # Entry point - keep it clean and minimal
├── auth.py              # Authentication logic only
├── fetch_courses.py     # Course fetching logic only
├── pdf_export.py        # PDF generation logic only
├── utils.py             # UI utilities only
└── requirements.txt     # Dependencies
```

### Module Responsibilities

- **main.py** - Application flow control only
- **auth.py** - Authentication, session management
- **fetch_courses.py** - API calls, data fetching, parsing
- **pdf_export.py** - PDF generation and formatting
- **utils.py** - Terminal UI, user interactions

## Testing Guidelines

Before submitting a PR, ensure:

- [ ] Authentication works correctly
- [ ] Course fetching succeeds
- [ ] PDF generation produces valid files
- [ ] Error handling works as expected
- [ ] Terminal UI displays correctly
- [ ] No crashes or unhandled exceptions

## Areas for Contribution

We're particularly interested in contributions for:

- **Performance improvements** - Faster data fetching
- **Error handling** - Better error messages and recovery
- **Features** - CSV export, filtering, sorting, etc.
- **Documentation** - Improved README, code comments
- **Testing** - Unit tests, integration tests
- **UI/UX** - Better terminal interface

## Questions?

Don't hesitate to ask questions! Create an issue with the `question` label.

## Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone.

### Our Standards

**Positive behavior includes:**
- Being respectful and inclusive
- Accepting constructive criticism gracefully
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Any unprofessional conduct

## Recognition

Contributors will be recognized in the project README. Thank you for making this tool better! 🙏

---

*Thank you for contributing to the EWU Course Fetching Tool!*

