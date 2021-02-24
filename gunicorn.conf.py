# gunicorn.conf.py
# Non logging stuff
bind = "0.0.0.0:7000"
workers = 3
# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn/gunicorn.error.log"
# Whether to send Nginx output to the error log 
capture_output = True
# How verbose the Gunicorn error logs should be 
loglevel = "DEBUG"