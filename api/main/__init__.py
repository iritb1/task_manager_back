from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from .config import config_by_name
import requests
import os
import sys
from api.main.model import config
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
import re


dirname = os.path.dirname(__file__)
# dirname = os.path.join(dirname, '..')
UPLOAD_FOLDER = os.path.join(dirname, r'../../../taskManagerData/attachments')

# config elastic logger
elastic_logger = logging.getLogger('elastic_logger')


def create_app(config_name):
    global elastic_logger
    STATIC_FOLDER = '../../static'
    # logs_file_handler = FileHandler('logs.txt', encoding='utf-8')
    # logs_file_handler.setLevel(DEBUG)
    # formatter = Formatter('%(asctime)s:%(name)s:%(message)s')
    # logs_file_handler.setFormatter(formatter)

    app = Flask(__name__,
                static_url_path='',
                static_folder=STATIC_FOLDER,
                template_folder=STATIC_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    CORS(app, supports_credentials=True)
    app.config.from_object(config_by_name[config_name])

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    if (app.debug):
        elastic_file_handler = logging.FileHandler(
            "api/logs/elastic_logs/elastic_logs.log")
        file_handler = logging.FileHandler(
            "api/logs/api_logs/api_logs.txt")
    else:
        elastic_file_handler = RotatingFileHandler(
            "api/logs/elastic_logs/elastic_logs.log", maxBytes=30*1000*1000, mode='w', encoding='utf-8', backupCount=3)

        file_handler = RotatingFileHandler(
            "api/logs/api_logs/api_logs.txt", maxBytes=30*1000*1000, mode='w', encoding='utf-8', backupCount=3)

    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)

    elastic_logger.setLevel(logging.INFO)

    elastic_file_handler.setLevel(logging.DEBUG)

    elastic_file_handler.setFormatter(formatter)

    elastic_logger.addHandler(stream_handler)
    elastic_logger.addHandler(elastic_file_handler)

    @ app.route('/')
    @ app.route('/<path>')
    @ app.route('/login')
    @ app.route('/monitor-fault/<id>')
    def catch_all(path=None, id=None):
        if (datetime.now() > config.cashe_time + timedelta(minutes=config.consts.CACHE_REFRESH_TIME["minutes"])):
            config.refresh_cache()
        return render_template("index.html")

    return app
