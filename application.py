import logging
import logging.handlers

from flask import Flask, request


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler 
LOG_FILE = '/opt/python/log/eb_worker.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

app = Flask(__name__)
@app.route('/', methods=['POST'])
def parse_request():
  if request.method == 'POST':
    try:
      request_body = request.get_json()
      logger.info("Received message: %s" % request_body)
    except (BadRequest):
      logger.warning('Error retrieving request body for async work.')
    response = 'received!'
  else:
    response = 'welcome!'
    return response # response to your request.

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
