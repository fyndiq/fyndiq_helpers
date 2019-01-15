# {{ cookiecutter.reponame|replace('-', ' ') }}

[![CircleCI integration](https://circleci.com/gh/fyndiq/{{ cookiecutter.reponame }}/tree/master.svg?style=shield&circle-token={{ cookiecutter.circleci_status_token }})](https://circleci.com/gh/fyndiq/{{ cookiecutter.reponame }}/tree/master)
[![CircleCI prod](https://circleci.com/gh/fyndiq/{{ cookiecutter.reponame }}/tree/prod.svg?style=shield&circle-token={{ cookiecutter.circleci_status_token }})](https://circleci.com/gh/fyndiq/{{ cookiecutter.reponame }}/tree/prod)
[![codecov](https://codecov.io/gh/fyndiq/{{ cookiecutter.reponame }}/branch/master/graph/badge.svg?token={{ cookiecutter.codecov_token }})](https://codecov.io/gh/fyndiq/{{ cookiecutter.reponame }})

## Purpose

This service...

## Getting started

See [Getting started](https://github.com/fyndiq/fyndiq-2.0#getting-started) for
instructions how to setup the development environment.

### Setup environment

    make setup
    source .venv/bin/activate

### Run service

    make run

### Run tests

    make test

### Run linter

    make lint

### Generate K8s manifests

    make manifests

## API reference

See [API reference](docs/api/README.md)
