# E-Commerce API

A production-ready RESTful API for e-commerce platform built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- Product Create and Get Feature
- Order processing with stock management
- Data validation using Pydantic
- Database migrations with Alembic
- Docker support for easy deployment
- Comprehensive test suite

## Requirements

- Python 3.12+
- PostgreSQL 16+
- UV package manager (optional, can use pip)

## Screenshots
1. Swagger UI

![Swagger UI](https://i.ibb.co/F4yPJmWT/image.png)


2. Tests Passing

![Tests Passing](https://i.ibb.co/rRNppY6N/image.png)

## Project Structure

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── product.py       # Product model
│   │   └── order.py         # Order model
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── product.py       # Product schemas
│   │   └── order.py         # Order schemas
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── products.py  # Product endpoints
│   │   │   └── orders.py    # Order endpoints
│   ├── crud/                # CRUD operations
│   │   ├── __init__.py
│   │   ├── product.py       # Product operations
│   │   └── order.py         # Order operations
│   ├── db/                  # Database connection
│   │   ├── __init__.py
│   │   └── database.py      # DB session management
│   └── exceptions/          # Custom exceptions
│       ├── __init__.py
│       └── http_exceptions.py
├── tests/                   # Test cases
│   ├── __init__.py
│   ├── conftest.py          # Test configurations and fixtures
│   ├── test_products/       # Tests directory for product
│   └── test_orders/         # Tests directory for order
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini              # Alembic configuration
├── .pre-commit-config.yml   # Pre-commit hooks config for better linting and formatting
├── .flake8.ini              # Flake8 configuration
├── .isort.cfg               # isort pre-commit hook config
├── .gitignore               # Git ignore config
├── .python-version          # Python version for this project
├── pyproject.toml           # Python project config file used by uv
├── sample.env               # Sample file for .env
├── Dockerfile               # Docker configuration for the app
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation

```


## Setup and Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-api
```

2. Create and activate a virtual environment:
```bash
uv venv

source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
# Using UV
uv sync

# Or using pip
pip install -e .
```

4. Create a .env file based on sample.env:
```bash
cp sample.env .env
```
NOTE: Chnage the .env config variables as per your setup

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
fastapi dev app/main.py
```

### Using Docker Compose

1. Make sure Docker and Docker Compose are installed

2. Create .env file from sample:

3. Build and start the containers:
```bash
docker compose up --build
```
The API will be available at http://0.0.0.0:8000

#### API Documentation
Once the server is running, you can access:

Swagger UI documentation: http://0.0.0.0:8000/docs
ReDoc documentation: http://0.0.0.0:8000/redoc


## Testing

Run the test suite:
```bash
pytest
```
For verbose output
```bash
pytest -v
```
