#!/usr/bin/env python3
#
# Run the OpenVPN server.
#
import sys
import click
import os
from ovnp_util import create_char_file
from subprocess import Popen, PIPE

SERVER = "192.168.255.0/24"
ROUTE = "192.168.254.0/24"

@click.command()
@click.option("-D", "--vpndir", envvar="OPENVPN", help="OpenVPN config directory")
def run(vpndir):
    create_char_file("/dev/net", "tun")
    add_iptable_rule(SERVER)
    add_iptable_rule(ROUTE)
    exec(f"/usr/sbin/openvpn --config {vpndir}/server.conf")

def add_iptable_rule(cidr):
    # Add iptables if they don't already exists - "-C" checks if they exist and "-A" appends rule if needed
    exec(f"/sbin/iptables -t nat -C POSTROUTING -s {cidr} -o eth0 -j MASQUERADE 2>/dev/null "
         f"|| /sbin/iptables -t nat -A POSTROUTING -s {cidr} -o eth0 -j MASQUERADE")

def exec(cmd):
    args = cmd.split()
    p = Popen(args, stdout=sys.stdout, stderr=sys.stderr)
    out, err = p.communicate()
    if p.returncode > 0:
        raise Exception("Command \"{}\" failed with return code #{}.".format(cmd, p.returncode))

if __name__ == '__main__':
    run()
