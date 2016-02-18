# Url Shortener Code

Python3 is needed to be have the application running, also postgresql-libs and a running instance of postgres
- Install dependencies with `make install`
- Create a database in your postgres and name it as the var DB_NAME
- set the environment variables  DB_USER, DB_PASS, DB_HOST, DB_PORT, and DB_NAME, while the first 4 defaults to something generally sensible
    as postgres, postgres localhost and 5432 the last one is up to what you set in the previous step, and it defaults to tiny_url
- now run the migrations with `make migrate`
- to test run `make test`, tests are mocked on the store layer, so they don't need a database to run and they don't actually hit the db
- to start the app run `make develop`, it will start the app on the port 5000 on localhost, go to localhost:5000/tiny to get the UI
