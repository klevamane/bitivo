#!/bin/bash

set +ex

#@--- Function to initialize gcloud ---@#
gcloud_initialize() {

    #@--- Create service account key ---@#
    touch service_key.json

    #@--- Decode the service acoount into json format ---@#
    echo $SERVICE_ACCOUNT | base64 -d > service_key.json

    #@--- Authenticate gcloud with the service account ---@#
    gcloud auth activate-service-account --key-file service_key.json

    #@--- Configure docker with gcloud credentials ---@#
    gcloud auth configure-docker --quiet
}

#@--- Function to build docker image for staging and production ---@#
build_staging_production_images() {
    #@---  If the branch is develop ---@#
    if [[ "${BRANCH_NAME}" == "develop" ]]; then

        echo " ++++++++++++++++++++++++++++ Building Staging Image ++++++++++++++++++++++++++++ "

        #@--- Load google credentials used to load hotdesk data ---@#
        eval $(echo $GOOGLE_CREDENTIALS_STAGING_ENCODED | base64 -d)

        #@--- copy env vars ---@#
        env >> .env

        #@--- replace the env value for deployment from 'testing' to 'staging' ---@#
        sed -i 's/testing/staging/g' .env

        CIRCLE_SHA1=$(echo $GIT_COMMIT | cut -c -17)

        #@--- replace the index to the one assigned to staging ---@#
        sed -i  "s|:6379\/7|:6379\/8|g" .env

        echo "DATABASE_URI=${STAGING_DB_URL}" >> .env

        #@--- Build docker image and push to GCR ---@#
        docker build -t gcr.io/${GCLOUD_ACTIVO_PROJECT}/activo-api-${DEPLOY_STAGING_ENV}:${CIRCLE_SHA1} -f docker-release/Dockerfile .
        docker push gcr.io/${GCLOUD_ACTIVO_PROJECT}/activo-api-${DEPLOY_STAGING_ENV}:${CIRCLE_SHA1}
    fi

    #@--- Build image for production ---@#
    if [[ "${BRANCH_NAME}" == "master" ]]; then

        echo " ++++++++++++++++++++++++++++ Building Production Image ++++++++++++++++++++++++++++ "

        #@--- Load google credentials used to load hotdesk data ---@#
        eval $(echo $GOOGLE_CREDENTIALS_PROD_ENCODED | base64 -d)

        #@--- Copy env vars ---@#
        env >> .env

        #@--- replace the env value for deployment from 'testing' to 'production' ---@#
        sed -i 's/testing/production/g' .env

        CIRCLE_SHA1=$(echo $GIT_COMMIT | cut -c -17)

        #@--- replace the index to the one assigned to production ---@#
        sed -i  "s|:6379\/7|:6379\/9|g" .env

        echo "DATABASE_URI=${PROD_DB_URL}" >> .env

        #@--- build docker image and push to GCR  ---@#
        docker build -t gcr.io/${GCLOUD_ACTIVO_PROJECT}/activo-api-${DEPLOY_PROD_ENV}:${CIRCLE_SHA1} -f docker-release/Dockerfile .
        docker push gcr.io/${GCLOUD_ACTIVO_PROJECT}/activo-api-${DEPLOY_PROD_ENV}:${CIRCLE_SHA1}
    fi
}


main() {
    #@--- Initailize_gcloud ---@#
    gcloud_initialize

    #@--- Run the function to build the images ---@#
    build_staging_production_images
}

#@--- Run the main function ---@#
main
