import logging
from . import Database

# Format and Get root logger
LOG_LEVEL = logging.INFO
logging.basicConfig(
    format='[%(asctime)s][%(levelname)-8s][%(name)-16s][%(lineno)d] %(message)s',
    level=LOG_LEVEL,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

class Instance(Database):

    # Creator
    def __init__(self, hostname, port=6032):
        self.auth_plugin    = None
        self.connection     = None
        self.hostname       = hostname
        self.port           = port
        self.schema         = "main"
        self.version        = None
        self.full_version   = None
        logger.setLevel(LOG_LEVEL)

class Hostgroup():

    # Creator
    def __init__(self, id):
        pass

class Server():

    # Creator
    def __init__(self, id):
        pass

class User():

    # Creator
    def __init__(self, id):
        pass

class Rule():
 
    # Creator
    def __init__(self, id):
        pass
