# To docker run PostgreSQL
 `docker run --env=POSTGRES_USER=admin --env=POSTGRES_PASSWORD=123gr --env=POSTGRES_DB=simplocialdb -p 5432:5432 -d --name simleocialdb postgres`

# To docker run Redis
 `docker run -d --name redis-secure -e REDIS_PASSWORD=123ger redis:latest redis-server --requirepass 123gr`