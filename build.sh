#!/bin/bash
pytest -vv --cov=ovpn --cov-fail-under=97 && pylint ovpn/*.py tests/*.py && docker build -t tfasz/openvpn .
