import logging


class ConfigValidationException(Exception):
    """
    Exception that is thrown if the config of class :class:`~issueshark.config.Config` could not be validated
    """
    pass


class Config(object):
    """
    Config object, that holds all configuration parameters
    """
    def __init__(self, args):
        """
        Initialization

        :param args: argumentparser of the class :class:`argparse.ArgumentParser`
        """
        self.host = args.db_hostname
        self.port = args.db_port
        self.user = args.db_user
        self.password = args.db_password
        self.database = args.db_database
        self.authentication_db = args.db_authentication
        self.num_cores = args.cores
        self.debug = args.debug
        self.start_index = args.start_index
        self.end_index = args.end_index
        self.ssl_enabled = args.ssl
        self.whitelist_emails = args.whitelist_emails

    def get_debug_level(self):
        """
        Gets the correct debug level, based on :mod:`logging`
        """
        choices = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        return choices[self.debug]

    def __str__(self):
        return "Config: host: %s, port: %s, user: %s, " \
               "password: %s, database: %s, authentication_db: %s, num_cores:%s, debug: %s, ssl: %s" % \
               (
                   self.host,
                   self.port,
                   self.user,
                   self.password,
                   self.database,
                   self.authentication_db,
                   self.num_cores,
                   self.debug,
                   self.ssl_enabled
               )



