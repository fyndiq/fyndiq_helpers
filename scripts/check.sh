#!/usr/bin/env sh
echo "Running mypy checks..."
mypy fyndiq_helpers/ --ignore-missing-imports --show-error-context
