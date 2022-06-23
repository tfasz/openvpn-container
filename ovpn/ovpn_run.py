#!/usr/bin/env python3
#
# Run the OpenVPN server.
#
import click
import os
from ovpn_util import create_char_file, exec_cmd

SERVER = "192.168.255.0/24"
ROUTE = "192.168.254.0/24"

@click.command()
@click.option("-D", "--vpndir", envvar="OPENVPN", help="OpenVPN config directory")
def run(vpndir):
    create_char_file("/dev/net", "tun")
    add_iptable_rule(SERVER)
    add_iptable_rule(ROUTE)
    exec_cmd(f"/usr/sbin/openvpn --config {vpndir}/server.conf")

def add_iptable_rule(cidr):
    # Add iptables if they don't already exists - "-C" checks if they exist and "-A" appends rule if needed
    exec_cmd(f"/sbin/iptables -t nat -C POSTROUTING -s {cidr} -o eth0 -j MASQUERADE 2>/dev/null "
         f"|| /sbin/iptables -t nat -A POSTROUTING -s {cidr} -o eth0 -j MASQUERADE")

if __name__ == '__main__':
    run()
