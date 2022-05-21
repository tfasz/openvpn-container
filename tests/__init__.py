# pylint: disable=import-error,missing-function-docstring,missing-module-docstring,wrong-import-position
import os.path
import shutil
import sys
test_dir = os.path.dirname(__file__)
temp_dir = os.path.join(test_dir, "temp")
sys.path.append(os.path.join(test_dir, "../ovpn"))
from ovpn_util import read_file

def get_expected_output_file(file_name):
    expected_output_dir = os.path.join(test_dir, "expected-output")
    return os.path.join(expected_output_dir, file_name)

def read_expected_output(file_name):
    return read_file(get_expected_output_file(file_name))

def read_temp_file(file_name):
    return read_file(os.path.join(temp_dir, file_name))

def rm_tree(delete_dir):
    if os.path.exists(delete_dir):
        shutil.rmtree(delete_dir)
