# RewriteForge Service

A lightweight FastAPI service that transforms plain text into different styles using LLM adapters.

## Run configuration

Configure the service using environment variables.

Copy `env.example` to `.env` and customize as needed.

## Run locally

``` bash
# Initialize Python virtual environment for the project
python -m venv venv

# Install the requirements
pip install -r requirements.txt

# Activate the virtual environment
source venv/bin/activate

# Setup .env file (copy template from .env.example) and set the environment variables
cp .env.example .env

# Run the FastAPI application
uvicorn app.main:app --reload
```

## Run locally as a Docker container


``` bash
docker-compose up --build
```

## Testing

``` bash
# Execute the unit tests:
pytest -v tests/unit


# Create a .env.test file (copy from .env.example) and set the test API KEY for OpenAI
cp .env.example .env.tst

# Execute the integration tests:
pytest -v tests/integration

# Run the tests coverage:
pytest --cov=app
```


### Run Fromatting and Linting

```bash
# Run linting checks
ruff check .

# Run linting with auto-fix
ruff check --fix .

# Run formatting
ruff format .
```

## API Endpoints

Check the generated Swagger documentation at http://localhost:8000/docs


## Architecture Decisions

### Layer Separation
- **HTTP Layer** (`main.py`): FastAPI routing and request/response handling
- **Business Logic** (`service.py`): Core rewriting logic and caching
- **Data Access** (`llm_adapter/`): LLM provider abstraction
- **Caching** (`cache/`): Caching abstraction and implementations (Redis and in-memory LRU cache)

### Caching Strategy
- In-memory cache using MD5 hash of the combination (text, style) as key
- Prevents redundant API calls for identical requests
- Works both for in-memory cache and for Redist implementation for the future

### Error Handling
- Input validation via Pydantic models
- LLM API error handling
- Proper HTTP status codes (400 for client errors, 500 for server errors)


### Future improvements

- Improve OpenAI LLM Adapter implemenetation by providing robust handling of errors, retries etc.
- Expose also metrics for the API calls - e.g. response time
- Add async queue mode and streaming
- Integrate Redis cache as an alternative to the already present in-memory one