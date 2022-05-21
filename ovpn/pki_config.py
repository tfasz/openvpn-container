"""Manage the PKI config for the VPN server"""
from subprocess import Popen, PIPE
from ovpn_util import load_config, render_template, write_file

class PkiConfig:
    """Manage PKI config for VPN server"""
    def __init__(self, vpn_dir, pki_dir, pki_bin_dir):
        self.vpn_dir = vpn_dir
        self.pki_dir = pki_dir
        self.easyrsa_vars_file = f"{vpn_dir}/easyrsa-vars"
        self.easyrsa_bin = f"{pki_bin_dir}/easyrsa"
        self.tls_crypt_key = f"{pki_dir}/tls-crypt.key"

    def exec(self, cmd):
        """Execute command with proper easyrsa environment variables set."""
        env = {"EASYRSA_PKI":self.pki_dir}
        args = cmd.split()
        with Popen(args, env=env, stdout=PIPE,  stderr=PIPE) as proc:
            proc.communicate()
            if proc.returncode > 0:
                raise Exception(f"Command \"{cmd}\" failed with return code #{proc.returncode}.")

    def exec_pki(self, cmd):
        """Execute easyrsa command with proper environment variables set"""
        self.exec(f"{self.easyrsa_bin} {cmd}")

    def init(self):
        """
        Initialize the PKI for our VPN server using the relevant config. This will build the
        folder structure, create a certificate authority to sign certs, generate the server certs,
        and create a secret we will use for TLS encryption of our VPN control channel.
        """
        config = load_config(self.vpn_dir)
        # Write vars file to ensure key types are configured correctly
        write_file(self.easyrsa_vars_file, render_template("easyrsa-vars.j2", config))

        # Provides a sufficient warning before erasing pre-existing files
        self.exec_pki("init-pki")

        # Generate server CA - don't set password on CA to keep it simple. Anyone with
        # access to this container will be able to generate client credentials.
        self.exec_pki("--batch build-ca nopass")

        # Create our secret for the TLS crypt key
        self.exec(f"/usr/sbin/openvpn --genkey secret {self.tls_crypt_key}")

        # For a server key with a password, manually init; this is autopilot
        self.exec_pki(f"build-server-full {config['common_name']} nopass")

        # Generate the CRL for client/server certificates revocation.
        self.exec_pki("gen-crl")
