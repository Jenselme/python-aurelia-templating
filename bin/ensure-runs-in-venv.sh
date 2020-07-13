#!/usr/bin/env bash

set -eu

readonly INSIDE_DOCKER=$(grep -q docker /proc/self/cgroup && echo true)
readonly command="$1"
# To be sure $@ will only contain the parameters of the command, not the command itself.
shift

# If we are already in a venv or if the are in docker, run directly.
if [[ -v VIRTUAL_ENV || "${INSIDE_DOCKER}" == "true" ]]; then
    echo "Already in venv"
    ${command} "$@"

    exit $?
else
    # Load bashrc to be sure PATH is correctly set. We can't do this before this it could mess up with the enabled venv.
    # We don't want to fail if the bashrc file contains unbound variables.
    set +u
    source ~/.bashrc || echo "Bash RC file not found"
    set -u
    # If not and pipenv is installed and we have a Pipfile, run with pipenv.
    if command -v pipenv > /dev/null && [[ -f Pipfile ]]; then
        echo "Running in venv with pipenv"
        pipenv run "${command}" "$@"

        exit $?
    # If poetry is installed and we have a pyproject.toml, run with poetry.
    elif command -v poetry > /dev/null && [[ -f pyproject.toml ]]; then
      echo "Running in venv with poetry"
      poetry run "${command}" "$@"
    else
        echo "Not in an virtual env and don't know how to run in one." >&2
        exit 1
    fi
fi
