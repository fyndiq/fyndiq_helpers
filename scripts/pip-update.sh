#!/usr/bin/env bash
pip-compile -U requirements/common.in --output-file requirements/common.txt
pip-compile -U requirements/test.in --output-file requirements/test.txt
