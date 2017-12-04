#!/usr/bin/env sh

CONFIG=test py.test  -x . --cov fyndiq_helpers/ --no-cov-on-fail
