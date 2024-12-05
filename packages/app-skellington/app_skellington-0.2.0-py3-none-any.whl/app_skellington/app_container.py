import functools
import inspect
import os

import appdirs

from . import _util, cfg, cli, log

# Application scaffolding:
from ._bootstrap import _bootstrap_logger

# These two variables affect the directory paths for
# config files and logging.
DEFAULT_APP_NAME = ""
DEFAULT_APP_AUTHOR = ""


class ApplicationContext:
    """
    Container for application-wide state; i.e. app configuration and loggers.
    """

    def __init__(self, config, log):
        self.config = config
        self.log = log
        self.parsed_argv = None
        self.parsed_argv_unknown = None


class ApplicationContainer:
    """
    Generalized application functionality. Used for linking components and modules of the application
    together. Invokes runtime configuration reading from file, maintains the
    object instances for services, passes off to the cli to determine what to
    do, and then injects any necessary dependencies (e.g. database module)
    and kicks off the functionality requested in the cli.

    Override appname and appauthor arguments to direct config and log
    directories.
    """

    def __init__(
        self, configspec_filepath=None, configini_filepath=None, *args, **kwargs
    ):
        self.appname = kwargs.get("appname") or DEFAULT_APP_NAME
        self.appauthor = kwargs.get("appauthor") or DEFAULT_APP_AUTHOR

        # Instantiate application context which contains
        # global state, configuration, loggers, and runtime args.
        self._dependencies = {}

        config = cfg.Config(configspec_filepath, configini_filepath)

        logger = log.LoggingLayer(self.appname, self.appauthor)
        # Try and load logging configuration if provided
        log_config = config.get("logging")
        if log_config is not None:
            logger.configure_logging(log_config)
        else:
            logger.configure_logging()

        self.ctx = ApplicationContext(config, logger)

        # Reference to root_app avail. in context
        self.ctx.root_app = self

        # Reference to context service avail. in root_app
        self["ctx"] = lambda: self.ctx

        self.cli = cli.CommandTree()  # Command-line interface

        # Run methods if subclass implemented them:
        if callable(getattr(self, "_cli_options", None)):
            self._cli_options()
        if callable(getattr(self, "_services", None)):
            self._services()
        if callable(getattr(self, "_command_menu", None)):
            self._command_menu()

    def __delitem__(self, service_name):
        """
        Deletes a service or dependency from the available dependencies.
        """
        try:
            del self._dependencies[service_name]
        except KeyError:
            pass

    def __getitem__(self, service_name):
        """
        Returns a factory of a service or dependency. The factory is a function
        that is called to return an instance of the service object.

        app['datalayer'] => returns the made-up "datalayer" service.
        """
        try:
            service_factory = self._dependencies[
                service_name
            ]  # Retrieve factory function
            return service_factory()  # Call factory() to return instance of service
        except KeyError:
            msg = "failed to inject service: {}".format(service_name)
            _bootstrap_logger.critical(msg)
            raise ServiceNotFound

    def __setitem__(self, service_name, value):
        """
        Register a service or dependency factory to return a service.

        The factory function is called to return an instance of a service object.
        """
        self._dependencies[service_name] = value

    def _construct_model(self, model_constructor, *args):
        """
        Performs dependency resolution and instantiates an object of given type.

        This takes in the reference to a class constructor and a list of names
        of the dependencies that need passed into it, constructs that object and
        returns it. Models contain business logic and application functionality.

        Args:
            model_constructor: reference to object constructor.
        """
        dependency_names = args
        dependencies = []
        for dep_name in dependency_names:
            dependencies.append(self[dep_name])
        return model_constructor(*dependencies)

    def _get_config_filepath(self, app_name, app_author, config_filename="config.ini"):
        """
        Attempt to find config.ini in the user's config directory.

        On Linux, this will be /home/<user>/.config/<app>/config.ini
        On Windows, this will be C:\\Users\\<user>\\AppData\\Local\\<app>\\config.ini
        """
        dirname = appdirs.user_config_dir(app_name, app_author)
        filepath = os.path.join(dirname, config_filename)
        _bootstrap_logger.info("default config filepath calculated to be: %s", filepath)
        return filepath

    def _get_configspec_filepath(self, configspec_filename="config.spec"):
        """
        Attempt to find config.spec inside the installed package directory.
        """
        return _util.get_root_asset(configspec_filename)

    def _inject_service_dependencies(self, constructor):
        """
        Returns a function that, when called, constructs a new object for
        business/application logic with the listed dependencies.

        Args:
            constructor: service class to be created object.
        """
        sig = inspect.signature(constructor.__init__)
        params = sig.parameters
        params = [
            params[paramname].name for paramname in params
        ]  # Convert Param() type => str
        cls_dependencies = params[1:]  # Skip 'self' parameter on class methods.

        return functools.partial(self._construct_model, constructor, *cls_dependencies)

    def load_command(self):
        args, unk, success = self.cli.parse()
        if not success:
            return False
        self.ctx.parsed_argv = args
        self.ctx.parsed_argv_unknown = unk
        return True

    def invoke_command(self):
        rc = self.load_command()
        if not rc:
            return False
        try:
            self.cli.run_command()
        except NoCommandSpecified:
            print("Failure: No command specified.")

    def interactive_shell(self):
        pass

    def invoke_from_cli(self):
        self.invoke_command()

    def usage(self):
        pass
        # Applications need a default usage


class ServiceNotFound(Exception):
    """
    Application framework error: unable to find and inject dependency.
    """

    pass


class NoCommandSpecified(Exception):
    pass
