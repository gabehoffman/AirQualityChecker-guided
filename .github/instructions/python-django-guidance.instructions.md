---
description: Python and Django-specific conventions and requirements for this project.
applyTo: "**/*.py"
---

# Python and Django Specifics

- Use a virtual environment for all development and deployment.
- Follow PEP 8 for code style and formatting.
- Organize Django apps logically; keep settings modular and use environment variables for secrets.
- Use Django's built-in security features (CSRF, XSS, SQL injection protection).
- Validate all user input and handle errors gracefully.
- Write tests for models, views, forms, and custom logic.
- Use Django's migration system for all database changes.
- Prefer class-based views for reusability and clarity.
- Document custom management commands, signals, and middleware.
- Avoid hardcoding values; use Django settings and configuration files.
