workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5
bind = "0.0.0.0:${PORT:10000}"
