# Proton Dynamic FS Quiz
This is the backed code for Proton Dynamic's Formula Student Quiz web app.

## Cloning
To clone this repo run:
```
git clone https://github.com/JulianKonowalski/fsquiz.git
```
The details of setting up the development environment are specified below.

## Development setup
To setup the development environment follow these steps:
- setup PostgreSQL locally (directly on the host/in a docker container or however you like)
- create a `.env` file in the root directory of this project containing the details specified below
- run `pip install -r requirements.txt` in the root directory of this project
- run `python scripts/createdb.py` script
- start up the app with `python src/main.py`

The app will run on localhost address on the port `5000`.

## example `.env` file
```
DB_NAME=my_database_name
DB_USERNAME=my_username
DB_PASSWORD=my_password
DB_HOST=my_host_url
DB_HOST_PORT=my_host_port
```