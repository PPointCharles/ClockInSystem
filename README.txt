ps -ef|grep gunicorn|awk '{print $2}'|xargs kill -9
gunicorn -D -w 4 -b 0.0.0.0:4000 app:app
