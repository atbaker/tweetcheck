# Gunicorn config

chdir = 'tweetcheck/'

bind = "0.0.0.0:8000"

workers = 1

accesslog = '-'
errorlog = '-'
