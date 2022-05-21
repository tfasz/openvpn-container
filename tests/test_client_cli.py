# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from click.testing import CliRunner
from ovpn_getclient import get_client
from tests import test_dir, read_expected_output

def test_client_cli():
    result = CliRunner().invoke(get_client, ["-D", test_dir, "test"])
    assert result.exit_code == 0
    assert result.output == read_expected_output("test-client.conf")

def test_client_cli_no_user():
    result = CliRunner().invoke(get_client, ["-D", test_dir, "fake-user"])
    assert result.exit_code == 1
