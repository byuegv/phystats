# -*- coding:utf-8 -*-
import codecs
import json
import logging
import logging.config

# Load the configuration.
config_file = "logging_conf.json"
with codecs.open(config_file, "r", encoding="utf-8") as fd:
    config = json.load(fd)

# Set up proper logging. This one disables the previously configured loggers.
logging.config.dictConfig(config["logging"])

logger = logging.getLogger()