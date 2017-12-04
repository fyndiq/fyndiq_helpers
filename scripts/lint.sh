#!/bin/bash
command -v flake8 >/dev/null 2>&1 || echo "flake8 is required"

echo "Running python linter..."
flake8