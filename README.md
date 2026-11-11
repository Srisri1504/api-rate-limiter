# API Rate Limiter & Monitoring Proxy

A lightweight, high-performance API Rate Limiter and Monitoring Proxy built with **Python** and **FastAPI**. It uses the **Sliding Window Log algorithm** to prevent API abuse and track real-time request metrics.

## Features
- **Sliding Window Rate Limiting:** Accurately restricts clients to a fixed number of requests per rolling time window.
- **Custom Middleware:** Intercepts incoming HTTP requests and returns `429 Too Many Requests` with a dynamic `Retry-After` header when limits are exceeded.
- **Real-Time Metrics:** Exposes monitoring endpoints to inspect allowed requests, blocked requests, and active client counts.
- **Automated Testing:** Includes unit and integration tests using `pytest`.

## Tech Stack
- **Language:** Python 3
- **Framework:** FastAPI, Uvicorn
- **Testing:** Pytest, HTTPX

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/data` | Protected endpoint limited to 5 requests per 60 seconds per IP. |
| `GET` | `/api/stats` | Returns live metrics (allowed/blocked counts and active clients). |
| `POST` | `/api/reset` | Resets rate limiter windows and clears current metrics. |

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd api-rate-limiter
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
5. Open `http://127.0.0` in your browser to test via Swagger UI.
