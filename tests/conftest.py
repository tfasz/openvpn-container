"""Location for pytest fixtures."""
import os
import pytest
from tests import test_dir

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Run cleanup logic at end of all tests"""
    def remove_crl():
        """"Clear CRL from test directory as it changes every time we run"""
        os.remove(os.path.join(test_dir, "crl.pem"))

    request.addfinalizer(remove_crl)
