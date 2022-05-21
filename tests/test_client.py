# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from client_config import ClientConfig
from ovpn_util import load_json
from tests import test_dir, get_expected_output_file

def test_client_config():
    expected_json = load_json(get_expected_output_file("test-client-conf.json"))

    # Generate the JSON data and validate
    client_config = ClientConfig(test_dir)
    data = client_config.get("test")
    assert data == expected_json
