## Activo

[![CircleCI](https://circleci.com/gh/andela/activo-api.svg?style=svg&circle-token=2df4d7cfe0bf14ef7398664e23ce48e17516815a)](https://circleci.com/gh/andela/activo-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/910afa389017caf8314a/maintainability)](https://codeclimate.com/repos/5c2f12229f0dc00240008913/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/910afa389017caf8314a/test_coverage)](https://codeclimate.com/repos/5c2f12229f0dc00240008913/test_coverage)

An asset-management tool for Andela

## Description

The **activo-api** is the backbone of an application for managing physical assets of the organisation. The project enables centralised management of assets of the organisation. The api provides features for registering the allocation and usage of assets, repairs and conditions of devices, allocation of computer devices and seat allocations.

The API documentation can be found here: [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0e1d7d5d1e5e38f14ea8)

## Key Application features

1. Inventory Management
2. Asset Allocations
3. Asset Maintenance & Repair logs

## Set Up Development With Docker (Preferred setup)

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account to download Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

-   `cd <project dir>` to check into the dir
-   `docker-compose build` or `make build` to build the application images
-   `docker-compose up -d` or `make start` or `make start_verbose` to start the api after the previous command is successful

The `docker-compose build` or `make build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

The `docker-compose up -d` or `make start` command starts the application while ensuring that the postgres database is seeded before the api starts.

The `make start_verbose` command starts the api verbosely to show processes as the container spins up providing for the visualization of errors that may arise.

To stop the running containers run the command `docker-compose down` or `make stop`

**NOTE**: If you are using `docker for development` then you should ensure that the _DATABASE_URI_ in your `.env` is this `postgres://postgres:backend@database:5432/activo` else the application would not be able to connect to the database.

**To Clean Up After using docker do the following**

1. In the project directory, run the command `bash cleanup.sh` or `make clean`
2. Wait for all images to be deleted.

**URGENT WARNING** PLEASE DO NOT RUN THE CLEAN-UP COMMAND ABOVE UNLESS YOU ARE ABSOLUTELY SURE YOU ARE DONE WITH THAT DEVELOPMENT SESSION AND HAVE NO DATA THAT WOULD BE LOST IF CLEAN-UP IS DONE!

**Alternative cleanup method**

Instead of using the above command, you can delete images with the command `docker rmi repository:tag`

You can can run the command `docker images` to see the image **repository:tag** you may want to delete

Delete the Database dir with the command `sudo rm -rf activo_db`

### Alternative Development set up

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.6.5
    ```

-   Install pipenv:

    ```
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.6.25
    ```
-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
    ```

-   Clone the activo-api repo and cd into it:

    ```
    git clone https://github.com/andela/activo-api.git
    ```

-   Install dependencies:

    ```
    pipenv install
    ```

-   Install dev dependencies to setup development environment:

    ```
    pipenv install --dev
    ```

-   Make a copy of the .env.sample file and rename it to .env and update the variables accordingly:

    ```
    FLASK_ENV = "development" # Takes either development, production, testing
    DATABASE_URI = "postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_DATABASE_NAME" # Development and production postgres db uri
    TEST_DATABASE_URI = "postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_TEST_DATABASE_NAME" # Testing postgres db uri
    JWT_PUBLIC_KEY = "" # Andela Authentication public key, obtained from the technology dept
    API_BASE_URL_V1 = "" # The base url for V1 of the API
    CLOUDINARY_API_SECRET= your cloudnary secret
    CLOUDINARY_API_KEY= your cloudinary api key
    CLOUDINARY_CLOUD_NAME = your cloudinary name
    USER_NAME = activo admin gmail account for sending mail
    PASSWORD = password of activo admin gmail account
    REDIS_URL = redis://redis:6379/0 <Replace with your redis server url if not using docker>
    SENDGRID_API_KEY = sendgrid api key
    ACTIVO_MAIL_USERNAME = activo@andela.com
    ```

-   Activate a virtual environment:

    ```
    pipenv shell
    ```

-   Apply migrations:

    ```
    flask db upgrade
    ```

-   If you'd like to seed initial data to the database:

    ```
    flask seed
    ```

    to seed everything or

    ```
    flask seed <resource>
    ```

    to seed a specific resource.

    allowed resources arguments are

    ```
    center, asset_category, space_type, space, asset, roles, user, permissions, resource, resource_access_levels
    ```

*   Run the application with either commands:

    ```
    python manage.py runserver
    ```

    or

    ```
    flask run
    ```

*   Should you make changes to the database models, run migrations as follows

    -   Migrate database:

        ```
        flask db migrate
        ```

    -   Upgrade to new structure:
        ```
        flask db upgrade
        ```

*   Deactivate the virtual environment once you're done:
    ```
    exit
    ```
*   **Running Redis server**
    -   You can either install redis by using the `docker setup` with `compose` which sets up redis for you along with the application.
        However, if you are not running docker, then you can simply run the command `bash redis.sh` in the root project directory, this will install redis for you (if not already installed) and also run/start the redis server for the first time on your local machine.

## Running Celery worker

-   Regardless of the setup you may be using, please endevour to update the `.env` file with the following keys and the appropriate values(`redis_server_url`):
    ```
     REDIS_URL=<Your_Redis_Server_URL>
    ```
-   If you are setting up with **docker/docker-compose**, please ensure the `keys=values` below mirror the content of your `.env`:
    ```
      REDIS_URL=redis://redis:6379/0
    ```
-   If you are setting up the application without Docker, and/or you also have your own Redis server hosted independent of this application and of your machine, edit the `.env` file with your redis server URL by replacing the default values with the following details:

    ```
      REDIS_URL=<Your_Redis_Server_URL>
    ```

    The different updates above must be done before you do `flask run` or `docker-compose build & docker-compose up`, depending on your app setup.

\*If you are not running the app with docker/docker-compose and would like to restart **redis/celery\***

-   To run redis after it has been stopped run `redis-server`

-   In a new terminal tab run the Celery Message Worker with:

    ```
      celery worker -A celery_worker.celery_app --loglevel=info
    ```

## Running Celery beat

-   After setting up the Celery worker, you need to start the `celery-beat` used to to trigger `celery` scheduled tasks

-   In a new terminal tab start `celery-beat` with:

    ```
      celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info
    ```

## Running Celery Flower

-   To run `celery flower` with the `docker-compose` setup, do the following:

    1. Build the application using the instruction in the **Set Up Development With Docker** section above.
    2. When the application starts and is accessible on `port 5000` as usual, visit `localhost:8888` in your browser to view the `celery flower` UI.

-   To run `Celery flower` without using your local application setup (Most useful for remote systems debugging).
    1. You would need the `redis` URL for the `Redis (local/cloud) instance` you intend to connect to in order to see scheduled tasks
    2. Run the following command to pull the docker image and start the container
       `docker run -d -p=1515:5555 mher/flower:latest celery flower --port=5555 --broker=<REDIS_URL>`
    3. After running the above command, visit `localhost:1515` in order to view celery flower UI.
       **NOTE** That the `<REDIS URL>` above should be the same as the one being passed to the `REDIS_URL` variable in the application.

## Running tests and generating report

On command line run:

```
pytest
```

To further view the lines not tested or covered if there is any,

An `htmlcov` directory will be created, get the `index.html` file by entering the directory and view it in your browser.

## Filtering on the API

Filtering is implemented using a query parser and a custom filter. Its usage is addressed on this [LINK](dynamic_filter.md)

## Contribution guide

##### Contributing

All proposals for contribution must satisfy the guidelines in the product wiki.
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2170023) to track the work done.

##### Pull Request Process

-   A contributor shall identify a task to be done from the [pivotal tracker](https://www.pivotaltracker.com/n/projects/2170023).If there is a bug , feature or chore that has not been included among the tasks, the contributor can add it only after consulting the owner of this repository and the task being accepted.
-   The Contributor shall then create a branch off the `develop` branch where they are expected to undertake the task they have chosen.
-   Contributors are required to activate the git pre-commit hook to auto format staged Python files to pep8 with yapf and check for residual pep8 linting errors using pylint.
    All commits are required to pass all checks from the pre-commit hook.
    The pre-commit hook can be installed as follows:
    Option 1: Copy the `hooks/pre-commit` file into the `.git/hooks` directory.
    You will need to do this every time the `hooks/pre-commit` file is changed.
    Option 2: Create a file `.git/hooks/pre-commit` then create a symlink to this file by running the command:
    `ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit`
    You will only need to do this once for your local repository.
-   Although highly discouraged, the pre-commit hook can be bypassed by passing the `--no-verify` flag to the commit command as follows:
    `git commit --no-verify -m "commit message"`
-   After undertaking the task, a fully detailed pull request shall be submitted to the owners of this repository for review.
-   If there any changes requested ,it is expected that these changes shall be effected and the pull request resubmitted for review.Once all the changes are accepted, the pull request shall be closed and the changes merged into `develop` by the owners of this repository.
