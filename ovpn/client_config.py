"""Output client config ovpn file contents for an existing user"""
import os
from ovpn_util import load_config, read_file, read_x509, ValidationException

class ClientConfig:
    """Load config and generate client ovpn file contents"""
    def __init__(self, vpn_dir):
        self.vpn_dir = vpn_dir
        self.vpn_config = load_config(vpn_dir)

    def get(self, name):
        """Get the clients config as a string"""
        pki_dir = f"{self.vpn_dir}/pki"
        client_key_file = f"{pki_dir}/private/{name}.key"
        if not os.path.exists(client_key_file):
            raise ValidationException(f"Unable to find client key for \"{name}\" - please generate one first.")
        data = self.vpn_config
        data["client_key"] = read_file(client_key_file)
        data["client_cert"] = read_x509(f"{pki_dir}/issued/{name}.crt")
        data["ca_cert"] = read_file(f"{pki_dir}/ca.crt")
        data["tls_crypt_key"] = read_file(f"{pki_dir}/tls-crypt.key")
        return data
