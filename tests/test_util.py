# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
from ovpn_util import load_config, read_file, read_x509, render_template, save_config
from tests import test_dir, get_expected_output_file

def test_load_config():
    config = load_config(test_dir, "sample-config.json")
    assert config["common_name"] == "vpn.example.com"
    assert config["dns_servers"][0] == "192.168.0.2"

def test_read_file():
    assert read_file(get_expected_output_file("test.txt")) == "FOO"

def test_read_x509():
    file_cert = read_x509(os.path.join(test_dir,"pki/issued/test.crt"))
    assert file_cert == TEST_CERT

def test_save_config():
    config_file_name = "temp/config.json"
    data = {}
    data["foo"] = "bar"
    save_config(data, test_dir, config_file_name)
    config = load_config(test_dir, config_file_name)
    assert config == data

def test_render_template():
    data = load_config(test_dir, "config.json")
    data["client_key"] = "foo-key"
    data["client_cert"] = "foo-cert"
    data["ca_cert"] = "foo-ca-cert"
    data["tls_crypt_key"] = "secret"
    output = render_template("client.ovpn.j2", data)
    assert output == CLIENT_CONF

TEST_CERT="""-----BEGIN CERTIFICATE-----
MIIDUzCCAjugAwIBAgIRANIhz+r+NvbzCfeoZXpxlOkwDQYJKoZIhvcNAQELBQAw
FjEUMBIGA1UEAwwLRWFzeS1SU0EgQ0EwHhcNMjIwNDMwMjM1NzQzWhcNMjQwODAy
MjM1NzQzWjAPMQ0wCwYDVQQDDAR0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
MIIBCgKCAQEAv6szd+9r/gjKbnadOMToAWmU79X9Sk3sId1kkxcyO/zAs0ho6jiz
/mrk1Cu9WYYFWLobESLwehfnEHVVf9jLLWC0US+OAz/6cpA6Kf6dnExS6jqWFB2H
sBDdgqn3dHdYuSYHNOGl81pNH31ayiS2F1x8k4EKoBicFffDCExa1Rp8Fa81WEff
4u6X3EU7P/NYEfY37yMM29ILjJ542nI8wrmBcHIqUjxbjoQc4MMhokfZZbY9+ZO8
6lzhjV03V4MjXFphNDdpb3efYbyL8VkCAI5MORk6CgIanrie9gDi1/JpibNTJs57
bV9rGXpYRLwOm3T1wKvYMuiLPkT2UOJ6sQIDAQABo4GiMIGfMAkGA1UdEwQCMAAw
HQYDVR0OBBYEFANwaqWKxG7UUT8KFjekLItZHWzVMFEGA1UdIwRKMEiAFNRFUfun
QOyf7NDFEQtDUtW+3RoLoRqkGDAWMRQwEgYDVQQDDAtFYXN5LVJTQSBDQYIUGequ
ntxUY9ZbIwuikkSJJqpQbQIwEwYDVR0lBAwwCgYIKwYBBQUHAwIwCwYDVR0PBAQD
AgeAMA0GCSqGSIb3DQEBCwUAA4IBAQAMH610nx+cVjlFNbKMhPU8ZT8m3f4wByVq
ljugqubkUCFvKOrk27qB7LTzk8yZtcf/Q/kfogwjd37zjyo7wXB1yhb9/cC8Sbss
TpGh1xUTiy4ocjSaauiofGbvdz62arRY8giG1cjt/fG4E7XE+FGOIrAPgaxBGlpB
1sRh5mS7RUBCkHSJLVYPjgpxWaQIIrs5MBTKeJjRVSL61YuP/3cm0gCR6rvaQCdh
ZIHSCQGlzBmLN9m8tW79vg7OxCN0jQ/8HEO9MIpIlurdzv/Iag3167P5dhMH9QX/
BwXbAh7sX4FRn0tuJjK6g/BgETJflMCCQ9U+J0Bg2oa7TEXBSw7i
-----END CERTIFICATE-----
"""

CLIENT_CONF="""client
nobind
dev tun
auth SHA256
remote-cert-tls server
remote vpn.example.com 1194 tcp4
verify-x509-name vpn.example.com name
tls-client
tun-mtu 1500
verb 3
<ca>
foo-ca-cert
</ca>
<cert>
foo-cert
</cert>
<key>
foo-key
</key>
<tls-crypt>
secret
</tls-crypt>"""
