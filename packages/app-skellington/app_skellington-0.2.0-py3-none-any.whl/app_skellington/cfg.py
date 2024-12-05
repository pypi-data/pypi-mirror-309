# The cfg module provides Config, the app_skellington service for interfacing
# config.ini files, environment variables (*todo), and
# application-wide configuration. The underlying mechanism is built on top of
# ConfigObj module and it's recommended to use config.spec files to define
# your available configuration of the relevant application.


import configobj
import validate

from ._bootstrap import _bootstrap_logger


class Config:
    """
    Structure to store application runtime configuration. Also contains
    functionality to load configuration from local site file.

    Provide config.spec - specification file which defines allowed parameters and types.

    Provide config.ini - configuration instance which contains values for any
    configuration arguments.
    """

    DEFAULT_CAPABILITIES = {
        "allow_options_beyond_spec": True,
    }

    def __init__(
        self, configspec_filepath=None, configini_filepath=None, capabilities=None
    ):
        self._config_obj = None  # must be type configobj.ConfigObj()
        self._configini_data = None
        self._configini_filepath = None
        self._configspec_data = None
        self._configspec_filepath = None
        self._has_accessed_internal_configobj = True
        self._has_changed_internally = True
        self._capability_enforce_strict_spec_validation = False

        # Register the files and parse provided config.spec and config.ini
        self.configspec_filepath = configspec_filepath
        self.configini_filepath = configini_filepath
        # NOTE(MG) Setters above trigger load_config()

    @property
    def config_obj(self):
        self._has_accessed_internal_configobj = True
        return self._config_obj

    # config_filepath:
    ###########################################################################
    @property
    def configini_filepath(self):
        """
        Config.ini filepath of site-specified configuration settings. File
        stored on user machine. Reloads config when set.
        """
        return self._configini_filepath

    @configini_filepath.setter
    def configini_filepath(self, value):
        self._configini_filepath = value
        self._has_changed_internally = True
        self.load_config()

    # configspec_filepath:
    ###########################################################################
    @property
    def configspec_filepath(self):
        """
        Config.spec filepath of site-specified configuration settings. File
        stored in module directory. Reloads config when set.
        """
        return self._configspec_filepath

    @configspec_filepath.setter
    def configspec_filepath(self, filepath):
        if filepath is None:
            _bootstrap_logger.debug("cfg - Clearing configspec")
            self._configspec_filepath = None
            self._configspec_data = None
            self._has_changed_internally = True
            self.load_config()
            return

        try:
            with open(filepath) as fp:
                data = fp.read()
                self._configspec_filepath = filepath
                self._configspec_data = data
                self._has_changed_internally = True
                _bootstrap_logger.debug(
                    "cfg - Set configspec and read contents: %s", filepath
                )
                self.load_config()
                return
        except OSError:
            _bootstrap_logger.critical(
                "cfg - Failed to find config.spec: file not found (%s)", filepath
            )
            raise OSError("Failed to read provided config.spec file")

        self.load_config()

    def __contains__(self, key):
        try:
            has_item = key in self._config_obj
            return has_item
        except KeyError:
            pass

    def __delitem__(self, key):
        """
        Deletes the configuration item identified by <key> in the internal
        configuration storage.
        """
        try:
            del self[key]
        except KeyError:
            pass

    def __getitem__(self, key):
        """
        Returns the value of the configuration item identified by <key>.
        """
        try:
            v = self._config_obj[key]
            if isinstance(v, str):
                return v
            else:
                # return self._config_obj[key].dict()
                return self._config_obj[key]
        except KeyError:
            raise

    def __setitem__(self, key, value):
        """
        Assigns the value of the configuration item
        identified by <key> as <value>.
        """
        self._config_obj[key] = value

    def get(self, key, default=None):
        """
        Attempt to retrieve configuration item, otherwise return default
        provided value.

        Similar to Dictionary.get()
        """
        try:
            v = self.__getitem__(key)
            return v
        except KeyError:
            return default

    def load_config(self, configspec_filepath=None, configini_filepath=None):
        # Set new arguments if were passed in:
        if configspec_filepath is not None:
            self.configspec_filepath = configspec_filepath
        if configini_filepath is not None:
            self.configini_filepath = configini_filepath

        # Load and validate configuration if possible:
        self._load_config_files()
        if self.configspec_filepath:
            rc = self._validate_config_against_spec()
            if not rc:
                if self._capability_enforce_strict_spec_validation:
                    raise RuntimeError("Failed to validate config.ini against spec.")
                return False
        return True

    def _load_config_files(self):
        config_spec = self.configspec_filepath
        config_ini = self.configini_filepath

        # interpolation='template' changes config file variable replacement to
        # use the form $var instead of %(var)s, which is useful to enable
        # literal %(text)s values in the config.
        try:
            self._config_obj = configobj.ConfigObj(
                infile=config_ini,
                # options
                configspec=config_spec,
                # encoding
                interpolation="template",
                # raise_errors
            )
            _bootstrap_logger.debug(
                "cfg - Parsed configuration. config.spec = %s, config.ini = %s",
                config_spec,
                config_ini,
            )
            return True

        except configobj.ParseError:
            msg = f"cfg - Failed to load config: error in config.spec configuration: {self.configspec_filepath}"
            _bootstrap_logger.error(msg)
            return False
        except OSError:
            msg = "cfg - Failed to load config: config.spec file not found."
            _bootstrap_logger.error(msg)
            return False
        except Exception as ex:
            _bootstrap_logger.error(ex)
            return False

    def _validate_config_against_spec(self):
        config_spec = self.configspec_filepath
        config_ini = self.configini_filepath

        # Hack the configobj module to alter the interpolation for validate.py:
        configobj.DEFAULT_INTERPOLATION = "template"

        # Validate config.ini against config.spec
        try:
            _bootstrap_logger.info("cfg - Validating config file against spec")
            val = validate.Validator()
            assert isinstance(
                self._config_obj, configobj.ConfigObj
            ), "expecting configobj.ConfigObj, received %s" % type(self._config_obj)
            # NOTE(MG) copy arg below instructs configobj to use defaults from spec file
            test_results = self._config_obj.validate(
                val, copy=True, preserve_errors=True
            )
            if test_results is True:
                _bootstrap_logger.info(
                    "cfg- Successfully validated configuration against spec. input = %s, validation spec = %s",
                    config_ini,
                    config_spec,
                )
                return True

            elif test_results is False:
                _bootstrap_logger.debug(
                    "cfg - Potentially discovered invalid config.spec"
                )

            else:
                self._validate_parse_errors(test_results)
                return False
        except ValueError:
            _bootstrap_logger.error(
                "cfg - Failed while validating config against spec. "
            )
            return False

    def _validate_parse_errors(self, test_results):
        _bootstrap_logger.critical("cfg - Config file failed validation.")
        for section_list, key, rslt in configobj.flatten_errors(
            self._config_obj, test_results
        ):
            _bootstrap_logger.critical(
                "cfg - Config error info: %s %s %s", section_list, key, rslt
            )
            if key is not None:
                _bootstrap_logger.critical(
                    "cfg - Config failed validation: [%s].%s appears invalid. msg = %s",
                    ".".join(section_list),
                    key,
                    rslt,
                )
            else:
                _bootstrap_logger.critical(
                    "cfg - Config failed validation: missing section, name = '%s'. msg = %s",
                    ".".join(section_list),
                    rslt,
                )

    def print_config(self):
        """
        Print configuration to stdout.
        """
        print("config:")

        self._config_obj.walk(print)
        for section in self._config_obj.sections:
            print(section)
            for key in self._config_obj[section]:
                print("    ", self._config_obj[section][key])


class EnvironmentVariables:
    def __init__(self):
        raise NotImplementedError
