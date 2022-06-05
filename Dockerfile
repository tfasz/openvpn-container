# Original credit: https://github.com/jpetazzo/dockvpn
FROM alpine:latest
LABEL maintainer="tfasz"

# Setup /opt/ovpn folder for all of our config scripts. We will later symlink shortcuts to this location.
ADD ./requirements.txt /opt/ovpn/requirements.txt
RUN apk add --update openvpn iptables bash easy-rsa python3 && \
    python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools && \
    pip3 install -r /opt/ovpn/requirements.txt && \
    ln -s /usr/share/easy-rsa/easyrsa /usr/local/bin && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*

# Needed by scripts
ENV OPENVPN=/etc/openvpn
ENV EASYRSA=/usr/share/easy-rsa \
    EASYRSA_VARS_FILE=$OPENVPN/easyrsa-vars \
    EASYRSA_PKI=$OPENVPN/pki

EXPOSE 1194/udp

ADD ./ovpn /opt/ovpn
RUN ln -s /opt/ovpn/ovpn_genconfig.py /usr/local/bin/ovpn_genconfig && \
    ln -s /opt/ovpn/ovpn_initpki.py /usr/local/bin/ovpn_initpki && \
    ln -s /opt/ovpn/ovpn_getclient.py /usr/local/bin/ovpn_getclient && \
    ln -s /opt/ovpn/ovpn_notify.py /usr/local/bin/ovpn_notify && \
    ln -s /opt/ovpn/ovpn_revokeclient.py /usr/local/bin/ovpn_revokeclient && \
    ln -s /opt/ovpn/ovpn_run /usr/local/bin/ovpn_run && \
    chmod a+x /opt/ovpn/ovpn_run /opt/ovpn/*.py
WORKDIR /etc/openvpn
CMD ["ovpn_run"]
