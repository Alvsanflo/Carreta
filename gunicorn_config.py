import multiprocessing
import os

# Configuración de Gunicorn
bind = f"0.0.0.0:{os.getenv('PORT', 8000)}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
