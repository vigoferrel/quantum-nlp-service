# QBTC Security Configuration

# Security Headers
security_headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# Rate Limiting Configuration
rate_limiting = {
    "requests_per_minute": 100,
    "burst_size": 20,
    "window_size": 60
}

# Authentication Settings
authentication = {
    "jwt_expiration_hours": 24,
    "password_min_length": 12,
    "require_2fa": True,
    "session_timeout_minutes": 30
}
