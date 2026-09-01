# gunicorn.conf.py
import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"  # Only localhost (NGINX will connect)

# Worker processes (2 * CPU cores + 1)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# Logging
accesslog = "/home/neptune/Desktop/flask-weather-quote-app/logs/gunicorn-access.log"
errorlog = "/home/neptune/Desktop/flask-weather-quote-app/logs/gunicorn-error.log"
loglevel = "info"

# Process name
proc_name = "flask-weather-quote-app"

# Timeouts
timeout = 120
graceful_timeout = 30

# Maximum requests per worker (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 100

# User/group (www-data is standard for web servers)
#user = "neptune"
#group = "www-data"

# Enable logging
capture_output = True
enable_stdio_inheritance = True
