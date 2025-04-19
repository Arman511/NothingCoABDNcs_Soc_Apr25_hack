"""Gunicorn configuration file."""

import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Gunicorn settings
workers = 2
threads = 4
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8080")
timeout = 120
max_requests = 1000
max_requests_jitter = 50
FORWARD_ALLOW_IPS = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}

# Logging settings
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-")  # "-" means stdout
errorlog = os.getenv("GUNICORN_ERROR_LOG", "-")

logger = logging.getLogger("gunicorn.error")
logger.setLevel(loglevel.upper())
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Gunicorn configuration loaded with logging enabled.")
