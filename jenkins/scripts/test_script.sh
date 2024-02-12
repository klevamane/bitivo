#!/bin/bash

set -e

#@--- Function to run the tests ---@#
run_api_tests() {
    #@--- Setup system locales ---@#
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8

    #@--- Load google credentials used to load hotdesk data ---@#
    eval $(echo $GOOGLE_CREDENTIALS_STAGING_ENCODED | base64 -d)

    #@--- Switch to the code folder  ---@#
    cd ${WORKSPACE}

    #@--- Activate the virtual environment ---@#
    source $(python3 -m pipenv --venv)/bin/activate

    #@--- Run the tests  ---@#
    pytest --cov=api/ tests --cov-report xml
    /tmp/cc-test-reporter format-coverage coverage.xml -t "coverage.py" -o "tmp/cc.testreport.json"

}

main() {
    #@--- Run the function that will run tests on the code ---@#
    run_api_tests
}

#@--- Run the main function ---@#
main
