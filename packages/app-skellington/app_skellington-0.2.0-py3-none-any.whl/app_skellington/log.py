import logging
import logging.config
import os

import appdirs

from . import _util
from ._bootstrap import _bootstrap_logger, _logger_name

DEFAULT_LOG_SETTINGS = {
    "formatters": {
        "colored": {
            "class": "colorlog.ColoredFormatter",
            # 'format': '%(log_color)s%(levelname)-8s%(reset)s:%(log_color)s%(name)-5s%(reset)s:%(white)s%(message)s'
            "format": "%(white)s%(name)7s%(reset)s|%(log_color)s%(message)s",
        }
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "debug",
            "formatter": "colored",
        }
    },
    "loggers": {
        "root": {
            "handlers": [
                "stderr",
            ],
            "level": "debug",
        },
        "app_skellington": {
            # 'handlers': ['stderr',],
            "level": "critical",
            "propagate": "false",
        },
    },
}


class LoggingLayer:
    def __init__(self, appname=None, appauthor=None):
        self.appname = appname or ""
        self.appauthor = appauthor or ""
        self.loggers = {}

    def __getitem__(self, k):
        """
        Returns Logger object named <k>.

        Example:
            log = LoggingLayer(...)
            log['db'].info('loaded database module')

        Args:
            k: the name of the logger to retrieve (k, i.e. key)
        """
        logger = self.loggers.get(k)
        if not logger:
            logger = logging.getLogger(k)
            self.loggers[k] = logger
        return logger

    def configure_logging(self, config_dict=None):
        """
        Set the logging level for the process. Verbosity is controlled by a
        parameter in the config.

        Advice: While DEBUG verbosity is useful to debug, it can produce too much
        noise for typical operation.
        """
        if config_dict is None:
            _bootstrap_logger.debug(
                "log - No application logging configuration provided. Using default"
            )
            config_dict = DEFAULT_LOG_SETTINGS

        self.transform_config(config_dict)

        try:
            _bootstrap_logger.debug("log - Log configuration: %s", config_dict)
            logging.config.dictConfig(config_dict)
            _bootstrap_logger.debug("log - Configured all logging")
        except Exception as ex:
            print("unable to configure logging:", ex, type(ex))

    def transform_config(self, config_dict):
        """
        Fix some incompatibilities and differences between the config-file logging
        parameters and the final config dictionary passed into the logging module.
        """
        # Version should be hard-coded 1, per Python docs
        if "version" in config_dict:
            if config_dict["version"] != 1:
                _bootstrap_logger.warn("logging['version'] must be '1' per Python docs")
        config_dict["version"] = 1

        self._add_own_logconfig(config_dict)

        # Replace logger level strings with value integers from module
        for handler in config_dict["handlers"]:
            d = config_dict["handlers"][handler]
            self._convert_str_to_loglevel(d, "level")

        # Replace logger level strings with value integers from module
        for logger in config_dict["loggers"]:
            d = config_dict["loggers"][logger]
            self._convert_str_to_loglevel(d, "level")

        # Implementation note:
        # app_skellington expects root logger configuration to be under 'root'
        # instead of '' (python spec) because '' is not a valid name in ConfigObj.
        try:
            if config_dict["loggers"].get("root") is not None:
                config_dict["loggers"][""] = config_dict["loggers"]["root"]
                del config_dict["loggers"]["root"]
        except Exception:
            _bootstrap_logger.warn(
                "was not able to find and patch root logger configuration from arguments"
            )

        # Evaluate the full filepath of the file handler
        if "file" not in config_dict["handlers"]:
            return

        if (
            os.path.abspath(config_dict["handlers"]["file"]["filename"])
            == config_dict["handlers"]["file"]["filename"]
        ):
            # Path is already absolute
            pass
        else:
            dirname = appdirs.user_log_dir(self.appname, self.appauthor)
            _util.ensure_dir_exists(dirname)
            log_filepath = os.path.join(
                dirname, config_dict["handlers"]["file"]["filename"]
            )
            config_dict["handlers"]["file"]["filename"] = log_filepath

    def _add_own_logconfig(self, config_dict):
        # NOTE(MG) Monkey-patch logger
        # This is done twice: once when app_skellington
        # module is imported again if logging configuration is
        # reloaded. This catches APPSKELLINGTON_DEBUG environment
        # variable the second time, when it's being reloaded as a
        # logging configuration is read from config file.
        # See _bootstrap.py
        if os.environ.get("APPSKELLINGTON_DEBUG", None):
            if _logger_name not in config_dict["loggers"]:
                config_dict["loggers"][_logger_name] = {
                    "level": "debug",
                    "propagate": "false",
                }
            else:
                config_dict["loggers"][_logger_name]["level"] = "debug"

    def _convert_str_to_loglevel(self, dict_, key):
        """
        Convert a dictionary value from a string representation of a log level
        into the numeric value of that log level. The value is modified in-place
        and is passed in by a dictionary reference and a key name.

        For example,
          d = {'loggers': {'cas': {'level': 'critical'}}}
          convert_str_to_loglevel(d['loggers']['cas'], 'level')
            =>
          d is now {'loggers': {'cas': {'level': logging.CRITICAL}}}
        """
        try:
            s = dict_[key]
        except KeyError:
            raise
        if s == "critical":
            dict_[key] = logging.CRITICAL
        elif s == "error":
            dict_[key] = logging.ERROR
        elif s == "warning":
            dict_[key] = logging.WARNING
        elif s == "info":
            dict_[key] = logging.INFO
        elif s == "debug":
            dict_[key] = logging.DEBUG
        elif s == "all":
            dict_[key] = logging.NOTSET
