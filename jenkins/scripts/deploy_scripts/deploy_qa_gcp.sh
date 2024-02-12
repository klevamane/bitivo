#!/bin/bash

set +ex

#@--- Function to run the deployment script  ---@#
run_qa_deployment_script() {
    cd /home/circleci/activo-infra
    chmod +x jenkins/scripts/api_deploy_scripts/deploy_to_qa.sh
    ./jenkins/scripts/api_deploy_scripts/deploy_to_qa.sh
}

#@--- Function to clone infrastructure repository  ---@#
clone_infrastructure_repository() {
    git clone -b develop ${INFRASTRUCTURE_REPO} /home/circleci/activo-infra
    touch /home/circleci/activo-infra/ansible/account.json
    #@--- Decode the encoded service account to json and save it to account.json file ---@#
    echo $SERVICE_ACCOUNT_QA | base64 -d  > /home/circleci/activo-infra/ansible/account.json
}

main() {
    cd ${WORKSPACE}

    #@--- Run the function to clone infrastructure repository ---@#
    clone_infrastructure_repository

    #@--- Run the deployments function ---@#
    run_qa_deployment_script
}

#@--- Run the main function ---@#
main
