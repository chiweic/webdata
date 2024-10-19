# Alchemist ==> webdata

Code examples for the SQLAlchemy article. (see https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy#heading-prerequisites)

we used this codebase to spawn off the basic on fastapi + sqlalchemy with pydantic validation on accessing data from ddm website.

The following steps are used when running everythong "local" (on a dev machine)

1. Database preparation: create a database call test, with username and password (see scrripts description - but manually)
2. verify the database connection with psql -h 'localhost' -p 5433 -d test
3. touch .env and put the postgresql connection string as DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/alchemist
4. pip install -r requirements.txt (this is based on my pip freeze on fastapi, sqlalchemy and pydantic, uvicoen stuff)
5. http://127.0.0.1:8000/api/docs should gives you a head-start
6. for one can start doing any query, you need to create table etc.,
7. Using alembic:
    a. alembic init -t async alembic # for asynchronous support
    b. modify env.py to reflect the sqlalchemy.url (should be loaded via environment not hard-coded)
       from webdata.config import settings
       config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    c. on the env.py you need to import all models that needs to be handled by alembic (all database models)
    d. then let alembic do the first migration: alembic revision --autogenerate -m "Initial tables"
    e. finally do you revision by typing alembic upgrade head (and once you change any definition, you should run this again...)

Steps on doing adding object to the code base (example: event)

1. get your head around pydantic model before getting into database, so atart on webdata/api/models.py
2. add codes on the database to support the sqlalchemy orm model
3. add a simple post on the routes to make sure things work
4. run alembic revision --autogenerate -m "adding events"
5. and alembic upgrade head (you should see the SQL statement generated from version from alembic folder)
6. tested under api/docs

Noted,

Although you migh be thinking that we can just iterate on alembic (generate, upgrade cycle), but the SQL statement
(alter column, table etc.,) only WORK when no existing record/data presented, otherwise you will run into none-NULL value 
(previous CRUD). So, delete all record when you debug a post/create for this to work.