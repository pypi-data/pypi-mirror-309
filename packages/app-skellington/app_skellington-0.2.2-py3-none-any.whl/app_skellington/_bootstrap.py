import logging
import os
import sys

# Check and gracefully fail if the user needs to install a 3rd-party dep.
libnames = ["appdirs", "configobj", "colorlog"]


def check_env_has_dependencies(libnames):
    rc = True
    for libname in libnames:
        try:
            __import__(libname)
        except ModuleNotFoundError as ex:
            print("Missing third-party library: ", ex, file=sys.stderr)
            rc = False
    return rc


if not check_env_has_dependencies(libnames):
    print("Unable to load program without installed dependencies", file=sys.stderr)
    raise ImportError("python environment needs third-party dependencies installed")

# Logger for before the application and logging config is loaded
# - used to log before logging is configured
_log_fmt = "%(levelname)-7s:%(message)s"
_logger_name = "skell"
_bootstrap_logger = logging.getLogger(_logger_name)

# NOTE(MG) Logger monkey-patch:
# This is done twice: once when app_skellington
# module is imported via _bootstrap.py and again if logging
# configuration is reloaded. This catches APPSKELLINGTON_DEBUG
# environment variable the first time, as app_skellington module
# is imported. See cfg.py
if os.environ.get("APPSKELLINGTON_DEBUG", None):
    _bootstrap_logger.setLevel(logging.DEBUG)  # Don't filter any log levels
    fmt = logging.Formatter(_log_fmt)
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    _bootstrap_logger.addHandler(handler)
    _bootstrap_logger.debug(
        "log - APPSKELLINGTON_DEBUG set in environment: Enabling verbose logging."
    )

# Logging is by default off, excepting CRITICAL
else:
    _bootstrap_logger.setLevel(logging.CRITICAL)
_bootstrap_logger.propagate = False

# NOTE(MG) Pretty sure the logger has the default handler too at this point.
# It's been related to some issues with the logger double-printing messages.
_bootstrap_logger.addHandler(logging.NullHandler())
