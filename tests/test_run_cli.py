# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from click.testing import CliRunner
from ovpn_run import run
from tests import test_dir, static_pki_dir, read_expected_output

def test_run_cli():
    result = CliRunner().invoke(run, ["-D", test_dir])
    assert result.exit_code == 0
