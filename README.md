Backend: [![coverage report](https://git.smartfactory.ch/[GROUP_NAME]/[PROJECT_NAME]/badges/develop/coverage.svg?job=test-backend)](https://git.smartfactory.ch/[GROUP_NAME]/[PROJECT_NAME]/commits/develop)

# django-templates - django-api-vue

Basic django template with API support and a frontend-stack used at smartfactory.

# Template features

*   Custom django-admin commands
    *   `./manage.py smf_startapp [app_name]`
*   Sentry-Integration
*   Support for `memcached`/`redis` caching
*   `.env.yaml`-file based configuration
*   Support for deployment using `fabric3`
*   CI-tooling using GitLab CI (see `.gitlab-ci.yml`)
*   Linting/Testing pre-configured
*   `django-rest-framework` pre-installed
*   JWT-based store for django users
*   Basic login/logout endpoints for API-based authentiation
*   Frontend stack based on Webpack 4 and VueJS 2.x
*   Material-Design based VueJS components using Vuetify
*   State-Management using vuex
*   Tests using Karma/Cypress

# Setup

1.  Download branch as archive.
2.  Unzip, run `git init` and `git flow init`.
3.  Run `git add .` and commit as the initial commit.
4.  Add remote `origin`, push master & develop.
5.  Install `pipenv` using `brew install pipenv`.
6.  (If you don't want `pipenv` to manage your virtual environment, create it **BEFORE** running the next step!)
7.  Run `pipenv install`.
8.  (optional) Configure nginx host.
9.  Create PSQL database using `createdb [name]`.
10. Copy `.env.example.yaml` to `.env.yaml` and configure it accordingly.
11. Run `./manage.py migrate`.
12. Run `./manage.py runserver`.

# Tests

## Backend

1.  Make sure you configured the project using the list above (update `pytest.ini`).
2.  Make sure your tests are written within modules called either `*_tests.py` or `tests_*.py`.
3.  Run `pytest`.
4.  Code coverage is being generated to directory `htmlcov`

## Frontend

1.  Make sure you configured the project using the list above.
2.  ???
3.  Run `yarn test`

# Deploying the project

## Setup

1.  Add your personal SSH-Key to the application-user's `authorized_keys` file on the destination host.
2.  Add the application-user's Public-Key as a deployment key to the GitLab-project (generate a key using `ssh-keygen`).
3.  Configure `fabfile.py` accordingly.

## Deployment

1.  Make sure you have all dependencies installed locally (using `pipenv install --dev`).
2.  Deploy to staging environment using `fab staging deploy`.
3.  Deploy to production environment using `fab production deploy`.
