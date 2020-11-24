
# Napleão

This application is a _fictional_ API to support resellers from a franchings network.

The resellers will be capable to manage sales and monitoring the cashback provided by a gamification strategy.

The name is a tribute to Napoleão, one of the minds behind the Malbec fragrance.

## build

We use [Make](https://www.gnu.org/software/make/), [Docker](https://docs.docker.com/compose/) and [Compose](https://docs.docker.com/compose/).

Clone the project and run `make build` to prepare the infra needed.

## run

Below some steps to get development environment ready

### env vars

Clone [.env.template](config/.env.template) and fill all the keys

### postgres and redis

`docker-compose up -d postgres redis` to ensure that database are ready

### migrations

`make migrate`

### first user

`make createsuperuser`

### up

`make up`

After that, the API must respond in `http://localhost:8080`