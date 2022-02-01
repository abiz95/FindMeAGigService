import time

from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %('
                                                                       f'threadName)s : %(message)s')
# logging.basicConfig(filename='logs/log-'+time.strftime("%Y-%m-%d")+'.log', level=logging.DEBUG, format=f'%(
# asctime)s %(levelname)s %(name)s %(' f'threadName)s : %(message)s')
