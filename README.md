# Alchemist ==> webdata

Code examples for the SQLAlchemy article. (see https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy#heading-prerequisites)

we used this codebase to spawn off the basic on fastapi + sqlalchemy with pydantic validation on accessing data from ddm website.

The following steps are used when running everythong "local" (on a dev machine)

1. Database preparation: create a database call test, with username and password (see scrripts description - but manually)
2. verify the database connection with psql -h 'localhost' -p 5433 -d test
3. touch .env and put the postgresql connection string as DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/alchemist

