from app_skellington.cli import CommandTree


class TestCli_e2e:
    def test_null_constructor_works(self):
        x = CommandTree()
        assert True == True
