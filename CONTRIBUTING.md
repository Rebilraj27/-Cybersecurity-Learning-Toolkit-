# Contributing to Cyber Toolkit

Thanks for your interest! 🎉

## Code of Conduct

- Be respectful and constructive
- **Never** share or promote illegal hacking
- All contributions must be for **ethical, educational** purposes

## How to Contribute

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-tool`
3. Write clean code with docstrings
4. Add tests in `tests/`
5. Run `pytest` — all tests must pass
6. Run `black toolkit/ tests/` to format
7. Commit & push
8. Open a Pull Request

## Adding a New Tool

1. Create `toolkit/your_tool.py`
2. Add to `toolkit/__init__.py` `__all__`
3. Add CLI subcommand in `cli.py`
4. Write `tests/test_your_tool.py`
5. Update README features table

## Style Guide

- **PEP 8** compliant
- Type hints where possible
- Docstrings for all public functions
- Keep functions small & testable

## Tests

```bash
pytest -v --cov=toolkit
