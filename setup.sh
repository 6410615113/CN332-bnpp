#! /bin/bash
if [ -d "./venv" ]; then
    echo "Virtual environment created"
else
    python -m venv .venv
    echo "Virtual environment created"
fi

if [ -d "./.venv/Scripts" ]; then
    .venv/Scripts/python -m pip install --upgrade pip
    echo "Pip updated"
    .venv/Scripts/python -m pip install -r requirement
    echo "Requirements installed"
    .venv/Scripts/pip freeze
else
    .venv/bin/python -m pip install --upgrade pip
    echo "Pip updated"
    .venv/bin/python -m pip install -r requirement
    echo "Requirements installed"
    .venv/bin/pip freeze
fi
