"""
utils/rate_limiter.py — Simple in-memory rate limiter middleware
"""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
RATE_LIMIT    = 60
WINDOW_SECS   = 60
_request_counts: dict[str, list] = defaultdict(list)
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now       = time.time()
    window    = _request_counts[client_ip]
    _request_counts[client_ip] = [t for t in window if now - t < WINDOW_SECS]
    if len(_request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")
    _request_counts[client_ip].append(now)
    return await call_next(request)
