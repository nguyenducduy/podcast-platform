exec gunicorn -w 4 -b 0.0.0.0:5000 -k gevent wsgi:app -e FLASK_ENV=production
