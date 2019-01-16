import json
import logging
import logging.config
import multiprocessing
import os

from pycoshark.utils import get_base_argparser

from identityshark.config import Config
from identityshark.identityshark import IdentitySHARK


def setup_logging(default_path=os.path.dirname(os.path.realpath(__file__))+"/loggerConfiguration.json",
                  default_level=logging.INFO):
        """
        Setup logging configuration

        :param default_path: path to the logger configuration
        :param default_level: defines the default logging level if configuration file is not found(default:logging.INFO)
        """
        path = default_path
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)


def start():
    """
    Starts the application. First parses the different command line arguments and then it gives these to
    :class:`~issueshark.issueshark.IssueSHARK`
    """
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Starting identitySHARK...")

    parser = get_base_argparser('Plugin to merge different developer identities.', '0.0.1')
    parser.add_argument('--project-name', help='ignored', default=None)
    parser.add_argument('--debug', help='Sets the debug level.', default='DEBUG',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--cores', help='Sets the number of cores to use.', default=multiprocessing.cpu_count(),
                        type=int)
    parser.add_argument('--start-index', help='Person number from which to start.', default=0, type=int)
    parser.add_argument('--end-index', help='Person number where to stop.', default=0, type=int)
    parser.add_argument('--whitelist-emails', help='Comma separated list of omail addresses that should be considered when matching, even if they are frequent.', default='')

    args = parser.parse_args()
    cfg = Config(args)

    logger.debug("Got the following config: %s" % cfg)
    identity_shark = IdentitySHARK()
    identity_shark.start(cfg)


if __name__ == "__main__":
    start()
