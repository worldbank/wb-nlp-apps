# gunicorn -w 4 -k gevent -b 0.0.0.0:8910 server:app
gunicorn -w 4 --threads 4 --timeout 604800 --chdir /home/wb536061/wb-nlp/APP/ --log-level debug -b 0.0.0.0:8910 server:app &> /home/wb536061/wb-nlp/APP/app.log
