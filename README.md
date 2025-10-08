# Mini DataCatalog Sample - Django DRF Application

## Overview
This project is a Mini DataCatalog Sample implemented using Django and Django REST Framework (DRF). The application allows users to upload data files (CSV/JSON), load data from PostgreSQL or Oracle databases, and query ETL-related metadata. It includes modern authentication, async tasks, logging, and email reporting.


## Postman Collection
- A postman_collection.json is included for testing all endpoints.
- Use it to verify functionality and response correctness.
- [live API documentation](https://www.postman.com/blue-capsule-887187/tata-mostafaghanbari-sample-project/documentation/h4f0wql/mini-data-catalog-api)

## Running the Application
1. First clone the project repo
2. Copy the example environment file:
```bash
cp .env.example .env
```
3. Start all services with Docker Compose:
```bash
docker-compose up -d
```
3. Services included:
- app – Django DRF backend
- db – PostgreSQL
- redis – For Celery
- celery – Async worker
- postfix – Email server

## Technologies Used
- **Django & Django REST Framework (DRF)** – Main backend framework and REST API implementation.
- **Poetry** – Dependency and environment manager for Python.
- **Celery + Redis** – For async tasks like parsing 
uploaded files or reading data from external databases.
- **Gunicorn** – Production-ready WSGI server for running the app.
- **Python-Decouple** – For managing environment variables.
- **PostgreSQL** – Main database for storing catalog metadata.
- **Postfix (Dockerized)** – For sending email notifications for non-2xx HTTP logs.
- **Simple-JWT** – Token-based authentication for users.
- **Docker & Docker Compose** – Containerization of services (app, Redis, Celery, DB, Postfix).



## Architecture
The project follows a **modular architecture**:
- Each section of the project, like `api` or `account`, is a separate module.
- Inside each module:
  - `urls.py` – Define routes.
  - `views.py` – Handle HTTP requests.
  - `services/` – Main business logic; each service file contains related logic.
  - `models.py` – Database models.
- The main logic lives in **services**, allowing for clean code separation and maintainability.



## Database Design
The system includes the following tables:
- **SchemaNames** – Stores schema information.
- **TableNames** – Stores table information; each table belongs to one schema.
- **EtlNames** – Stores ETL processes.
- **EtlTableRel** – Many-to-many relationship between `TableNames` and `EtlNames`.



## Authentication
- Modern OTP-based authentication:
  - User enters email.
  - Receives OTP for verification.
  - If user does not exist, they are signed up automatically.
  - Returns JWT token pairs for authenticated access.
- Uses Django’s built-in User model for storing users.



## Logging & Email Reporting
- Middleware logs all **non-2xx HTTP responses** as errors.
- Errors are sent via email using `AdminEmailHandler` and the Dockerized Postfix service.

## Async Tasks
- Celery handles background tasks such as:
  - Parsing uploaded CSV/JSON files.
  - Reading data from external databases.



## API Endpoints

- All endpoints are defined using DRF with serializers for validation.
- Endpoint structure example:
  - POST /api/data/file/ – Upload data files.
  - GET /api/etl/{etl_name}/tables/ – Get tables related to a specific ETL.
- Full Postman collection is included in postman_collection.json.

