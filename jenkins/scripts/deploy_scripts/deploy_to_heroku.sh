#/bin/bash

set +ex

#@--- Function to deploy to heroku  ---@#
deploy_to_heroku() {
    if [[ "${BRANCH_NAME}" == "develop" ]]; then

        #@--- Load google credentials used to load hotdesk data ---@#
        eval $(echo $GOOGLE_CREDENTIALS_STAGING_ENCODED | base64 -d)

        #@--- copy env vars into the instance  ---@#
        env >> .env
        cat .env

        #@--- install heroku CLI  ---@#
        curl https://cli-assets.heroku.com/install.sh | sh

        #@--- Authenticate docker to heroku registry ---@#
        docker login --username=$HEROKU_LOGIN --password=$HEROKU_API_KEY registry.heroku.com

        #@--- login to heroku docker registry ---@#
        heroku container:login

        CIRCLE_SHA1=$(echo $GIT_COMMIT | cut -c -17)

        #@--- NOTICE ---@#

        #@--- if you are sharing the dyno with a new user ---@#
        #@--- ensure that you add the user as a collaborator ---@#
        #@--- else they would not be able to push images to the ---@#
        #@--- the Heroku registry. ---@#

        #@--- Build docker image for the docker container ---@#
        #@--- Tag and Push image to heroku container registory ---@#
        docker build -t registry.heroku.com/activo-new-testing/activo-api-${DEPLOY_STAGING_ENV}:${CIRCLE_SHA1} -f docker-heroku/Dockerfile .
        docker tag registry.heroku.com/activo-new-testing/activo-api-${DEPLOY_STAGING_ENV}:${CIRCLE_SHA1} registry.heroku.com/activo-new-testing/web
        docker push registry.heroku.com/activo-new-testing/web 

        #@--- re-tag docker image for another sandbox env and push ---@#
        docker tag registry.heroku.com/activo-new-testing/activo-api-${DEPLOY_STAGING_ENV}:${CIRCLE_SHA1} registry.heroku.com/e2e-api-develop/web
        docker push registry.heroku.com/e2e-api-develop/web

        #@--- release built application to activo-new-testing dyno ---@#
        heroku container:release web -a activo-new-testing

        #@--- release application application to e2e-develop-api dyno ---@#
        heroku container:release web -a e2e-api-develop
    fi
}


main() {
    #@--- Run the deploy to heroku function ---@#
    deploy_to_heroku
}

#@--- Run the main function ---@#
main
