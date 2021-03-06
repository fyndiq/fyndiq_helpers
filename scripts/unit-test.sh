#!/bin/bash
set -e
CONFIG=test pytest --cov=fyndiq_helpers/ --junitxml=/tmp/test-results/report.xml --no-cov-on-fail --cov-report term-missing

if [[ ! -z "${CODECOV_TOKEN}" ]]; then
    codecov -t $CODECOV_TOKEN
fi
