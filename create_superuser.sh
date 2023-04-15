#!/bin/sh
docker exec -it graphql_app sh -c "python create_superuser.py '$1' '$2'"