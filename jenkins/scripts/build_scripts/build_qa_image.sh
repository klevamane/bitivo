#!/bin/bash

set +ex

#@--- Function to initialize gcloud ---@#
gcloud_initialize() {

    #@--- Create service account key ---@#
    touch service_key.json

    #@--- Decode the service acoount into json format ---@#
    echo $SERVICE_ACCOUNT_QA | base64 -d > service_key.json

    #@--- Authenticate gcloud with the service account ---@#
    gcloud auth activate-service-account --key-file service_key.json

    #@--- Configure docker with gcloud credentials ---@#
    gcloud auth configure-docker --quiet
}

#@--- Function to build image optimized for the QA environment ---@#
build_qa_image() {
    if [[ "${BRANCH_NAME}" == "master" ]]; then

        echo "++++++++++++++++++++++ Building QA Image ++++++++++++++++++++++ "

        #@--- Load google credentials used to load hotdesk data ---@#
        eval $(echo $GOOGLE_CREDENTIALS_PROD_ENCODED | base64 -d)

        #@--- copy env vars ---@#
        env >> .env

        echo "++++++++++++++++++++++ Contents of the .env file ++++++++++++++++++++++ "
        cat .env
        echo "++++++++++++++++++++++ Listing contents Completed! ++++++++++++++++++++++ "

        CIRCLE_SHA1=$(echo $GIT_COMMIT | cut -c -17)

        #@--- replace the env value for deployment from 'testing' to 'staging' ---@#
        sed -i 's/testing/production/g' .env
        echo "DATABASE_URI=${DATABASE_URI_QA}" >> .env

        #@--- build docker image and push to GCR Andela-Learning ---@#
        docker build -t gcr.io/${GCLOUD_ACTIVO_PROJECT_QA}/activo-api-${DEPLOY_ENV_QA}:${CIRCLE_SHA1} -f docker-release/Dockerfile .
        docker push gcr.io/${GCLOUD_ACTIVO_PROJECT_QA}/activo-api-${DEPLOY_ENV_QA}:${CIRCLE_SHA1}
    fi

}

main() {
    #@--- Initailize_gcloud ---@#
    gcloud_initialize

    #@--- Run the function to build the qa image ---@#
    build_qa_image
}

#@--- Run the main function ---@#
main
