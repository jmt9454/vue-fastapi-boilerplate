🤖 Project Context & Coding Standards

1. Project Overview

This is a student management application using a FastAPI (Python) backend and a Vue 3 + Vuetify frontend.

Architecture: Layered Architecture (Router -> Service -> CRUD -> Models).

Database: SQLite (Local), PostgreSQL (Prod).

Package Manager: uv (Python), npm (Node).

2. Backend Rules (FastAPI)

Structure: All business logic must exist in services/. Routers should only handle request parsing and response formatting.

Database: Use Session dependency injection. NEVER import the global db session directly.

Pydantic: Use StudentCreate for inputs and StudentResponse for outputs. Always set from_attributes = True in config.

Testing: Use pytest with conftest.py override for in-memory SQLite DB.

Imports: Use absolute imports (e.g., from app.models import Student).

3. Frontend Rules (Vue 3)

Composition API: Always use <script setup>.

HTTP: All API calls must go through src/services/api.js. Do not use axios directly in components.

UI Library: Use Vuetify components (<v-card>, <v-btn>) instead of raw HTML/CSS where possible.

State: Use local ref for simple component state.

4. Code Style

Python: Follow PEP8.

JavaScript: Use ESLint standards.

Comments: Explain "Why", not "What".
