#!/bin/sh
docker exec -it graphql_app sh -c "flask create-superuser '$1' '$2'"