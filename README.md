# Setting up GEARBOx backend

## Run Docker Compose

```sh
docker-compose up
```

This operations starts the DB and the API services. The API service will be available at `0.0.0.0:5000`. Visit the root (`/`) path to see the generated API documentation.

## Load data

1. Create a `/Secrets/creds.json` to set the `client_id` for fence
   - The app container will fail/crash without `Secrets/creds.json`. You can use the following dummy credential:

```json
{
  "CLIENT_ID": ""
}
```

2. Prepare files for trials data
   - Trials data files have to be obtained separately. (Talk to Tom.)
3. Modify `/load_trials.py` to use correct data files location
   - Change `data_path` and `data_prefix`
   - Default values:

```py
data_path = '~/Desktop/tables/'
data_prefix = 'v17/load_trials_v17 - '
```

4. Install dependencies

```bash
# set up and use virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# install pip dependencies
pip install -r requirements.txt
```

5. Run `/load_trials.py` to load trials data to the database
   - Stdout shows `201`s when new table rows are successfully created from the loaded data

## Run test

> :warning: To enable test, first set the environment variable `BOILERPLATE_ENV` to `test`. You can use `./config.env` for this.

CRUD tests can be run from the app container.

```sh
# 1. Get an interactive shell for the `app` container
docker-compose exec app sh

# 2. Start pipenv
pipenv shell

# 3. Run tests
pytest
```

Tests use (and require) the pre-set data, in `./db/pedal_populate.sql`.

When running tests, new data is created in the tests themselves and flushed from the session at the end of the tests.

Some tables use the `"code"` field, which can be used as a lookup code. Those that do not have `"code"` use primary keys, packages as dash separated ids (int), i.e. using the format `{}-{}-...`.

## Stop Docker Compose

```sh
docker-compose down
```

This operation also clears the DB.
