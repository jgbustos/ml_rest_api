#!/bin/bash
echo -e "\033[1;34m---------- Reformating with black... ----------\033[0m"
black ./ml_rest_api ./tests
echo -e "\033[1;34m---------- Analysing with pylint... -----------\033[0m"
pylint --recursive=y ./ml_rest_api ./tests
echo -e "\033[1;34m---------- Validating with mypy... ------------\033[0m"
mypy --pretty --config-file=mypy.ini ./ml_rest_api
