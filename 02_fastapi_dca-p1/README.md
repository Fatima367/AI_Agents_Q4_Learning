# Simple FastAPI Project with UV
This is a simple FastAPI project. Follow the steps below to setup and run the project

## Requirement

- Python 3.8 or above
- `uv` package manager (to run the app)
- `fastapi` (web framework)
- `pytest` and `pytest-asyncio` for testing (optional)

## Setup

1. **Create Virtual Environment**:
    ```bash
    uv init . 
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On macOS/Linux
    ```

2. **Install Dependencies**:
    ```bash
    uv add fastapi[standard]   # Install FastAPI
    uv add --dev pytest pytest-asyncio   # Install testing dependencies
    ```

3. **Run the server**:
    ```bash
    fastapi dev main.py
    ```
