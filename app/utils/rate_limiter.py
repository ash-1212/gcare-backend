"""
Simple in-memory rate limiter for public write endpoints.

Applies to: /auth/login, /contact, /newsletter/subscribe, /booking-requests
Section 12: Security — e.g. 5 req/min/IP.

NOTE: This is an in-memory implementation suitable for a single-process
MVP deployment. It resets on server restart and does not share state
across multiple worker processes. Flagged for Phase 2 (Redis-backed).
"""

import time
from collections import defaultdict

from fastapi import HTTPException, Request, status


class RateLimiter:
    """
    Sliding-window rate limiter keyed by client IP.

    Usage as a FastAPI dependency:
        @router.post("/booking-requests", dependencies=[Depends(RateLimiter(max_requests=5, window_seconds=60))])
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Maps client IP -> list of request timestamps within the current window
        self._requests: dict[str, list[float]] = defaultdict(list)

    def __call__(self, request: Request) -> None:
        client_ip = self._get_client_ip(request)
        now = time.time()

        # Drop timestamps outside the current sliding window
        self._requests[client_ip] = [
            ts for ts in self._requests[client_ip] if now - ts < self.window_seconds
        ]

        if len(self._requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

        self._requests[client_ip].append(now)

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """
        Resolve the real client IP, accounting for reverse proxies
        (e.g. Render/Railway/Vercel place the original IP in X-Forwarded-For).
        """
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown" 