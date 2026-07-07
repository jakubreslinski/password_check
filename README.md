# Password Strength Evaluation API

## How passwords are evaluated

1. **`zxcvbn`** – A library created by the team at Dropbox. It is a robust password strength estimator that takes into account over 30k common passwords, names, surnames, popular English words, patterns like dates, repeats or sequences, and l33t speak.
2. **Custom security rules** – My additional checks that are not natively included in the `zxcvbn` function: enforcing a minimal number of characters, requiring different types of characters (uppercase, lowercase, digits, symbols), and strictly blocking passwords that directly include the user's username or email address.

Based on combined evaluation, API returns score ranging from 0 to 4, along with suggestions and warnings about the password.

- **0** – Very Weak 
- **1** – Weak
- **2** – Fair
- **3** – Strong
- **4** – Very Strong

## How to run project

### Option 1: Docker

1. Clone and enter repository:

```bash
git clone https://github.com/jakubreslinski/password_check.git
cd password_check
```

2. Create docker image: 

```bash
docker build -t password-api .
```

3. Run docker container (add -d flag for detaching from server logs)

```
docker run -p 8000:8000 password-api
```

### Option 2: Locally (Python)

This project is using uv for dependency management

1. Clone and enter repository:

```bash
git clone https://github.com/jakubreslinski/password_check.git
cd password_check
```

2. Install dependencies

```bash
uv sync
```

3. Start server

```bash
uv run python main.py
```

## API Documentation and Usage

This API uses **FastAPI**, which automatically generates interactive API documentation based on the OpenAPI standard and Pydantic models.

Once the server is running (either via Docker or locally), you can interact with the API in two ways:

### 1. Interactive Web Interface (Swagger UI)
Open your browser and navigate to:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs) (Allows you to test endpoints directly from the browser)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc) (Alternative, read-only documentation format)

### 2. Command Line (cURL)
You can easily test the endpoint directly from your terminal using `curl`. Here is an example of a POST request:

```bash
curl -X POST "http://localhost:8000/api/v1/evaluate" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test.user@example.com", "password": "MySuperPassword123!@#"}'
```

## Running tests

To run automated tests, you need local Python environment. Once setup, run this command

```bash
uv run pytest
```
