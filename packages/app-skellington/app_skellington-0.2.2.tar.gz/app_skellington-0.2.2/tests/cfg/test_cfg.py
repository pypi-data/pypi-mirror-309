import pytest

from app_skellington import _util
from app_skellington.cfg import Config


@pytest.fixture
def sample_configspec_filepath():
    return _util.get_asset(__name__, "sample_config.spec")


@pytest.fixture
def sample_configini_filepath():
    return _util.get_asset(__name__, "sample_config.ini")


@pytest.fixture
def sample_full_configspec_filepath():
    return _util.get_asset(__name__, "sample_config_full.spec")


@pytest.fixture
def sample_full_configini_filepath():
    return _util.get_asset(__name__, "sample_config_full.ini")


@pytest.fixture
def sample_invalid_configspec_filepath():
    return _util.get_asset(__name__, "sample_config_invalid.spec")


class TestConfig_e2e:
    def test_allows_reading_ini_and_no_spec(self, sample_configini_filepath):
        cfg = Config(configini_filepath=sample_configini_filepath)
        assert (
            cfg["root_option"] == "root_option_val"
        ), "expecting default from config.spec (didnt get)"
        assert (
            cfg["app"]["sub_option"] == "sub_option_val"
        ), "expecting default for sub option"

    def test_allows_reading_spec_and_no_ini(self, sample_configspec_filepath):
        cfg = Config(configspec_filepath=sample_configspec_filepath)
        assert (
            cfg["root_option"] == "def_string"
        ), "expecting default from config.spec (didnt get)"

    # NOTE(MG) Changed the functionality to not do it this way.
    # def test_constructor_fails_with_invalid_spec(
    #     self, sample_invalid_configspec_filepath
    # ):
    #     with pytest.raises(Exception):
    #         cfg = Config(
    #             configspec_filepath=sample_invalid_configspec_filepath
    #         )

    def test_allows_options_beyond_spec(self, sample_configspec_filepath):
        cfg = Config(configspec_filepath=sample_configspec_filepath)
        cfg["foo"] = "test my value"
        assert cfg["foo"] == "test my value"

        cfg["app"]["bar"] = "another value"
        assert cfg["app"]["bar"] == "another value"

    # def test_can_read_config_file_mutiple_times(self):
    #     pass

    def test_can_override_config_file_manually(self, sample_configini_filepath):
        cfg = Config(configini_filepath=sample_configini_filepath)
        cfg["root_option"] = "newval"
        assert cfg["root_option"] == "newval"

        cfg["app"]["sub_option"] = "another_new_val"
        assert (
            cfg["app"]["sub_option"] == "another_new_val"
        ), "expecting default for sub option"

    def test_can_set_option_without_config(self):
        cfg = Config()
        cfg["foo"] = "test my value"
        assert cfg["foo"] == "test my value"

        cfg["app"] = {}
        cfg["app"]["bar"] = "another value"
        assert cfg["app"]["bar"] == "another value"

    def test_uses_spec_as_defaults(self, sample_configspec_filepath):
        cfg = Config(configspec_filepath=sample_configspec_filepath)
        assert (
            cfg["root_option"] == "def_string"
        ), "expecting default from config.spec (didnt get)"
        assert cfg["app"]["sub_option"] == "def_sub", "expecting default for sub option"
