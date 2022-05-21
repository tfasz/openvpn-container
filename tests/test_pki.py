# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
import pytest
from pki_config import PkiConfig
from ovpn_util import read_file
from tests import test_dir, read_expected_output, rm_tree

def test_pki_config():
    # Generate the JSON data and validate
    pki_dir = os.path.join(test_dir, "temp/pki")
    rm_tree(pki_dir)
    config = PkiConfig(test_dir, pki_dir, "/usr/share/easy-rsa")
    config.init()
    assert read_file(os.path.join(test_dir, "easyrsa-vars")) == read_expected_output("easyrsa-vars")

def test_pki_error():
    pki_dir = os.path.join(test_dir, "temp/pki")
    rm_tree(pki_dir)
    config = PkiConfig(test_dir, pki_dir, "/usr/share/easy-rsa")
    with pytest.raises(Exception):
        config.exec_pki("invalid-argument")
