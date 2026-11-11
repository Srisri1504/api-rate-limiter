from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from limiter import SlidingWindowRateLimiter

app = FastAPI(title="API Rate Limiter & Monitoring Proxy")
limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path.startswith("/api/data"):
        client_ip = request.client.host if request.client else "unknown"
        allowed, retry_after = limiter.is_allowed(client_ip)
        
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "Too Many Requests", "retry_after_seconds": retry_after},
                headers={"Retry-After": str(retry_after)}
            )
            
    return await call_next(request)

@app.get("/api/data")
def get_protected_data():
    return {"status": "success", "data": "Sensitive payload delivered."}

@app.get("/api/stats")
def get_stats():
    return {
        "max_requests_per_window": limiter.max_requests,
        "window_seconds": limiter.window_seconds,
        "active_clients": len(limiter.requests),
        "metrics": limiter.stats
    }

@app.post("/api/reset")
def reset_limiter():
    limiter.reset()
    return {"message": "Rate limiter state and metrics reset."}
