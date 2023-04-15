from modules.db_gateways.workers_gateway import WorkersGateway
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from os import environ
import sys


if __name__ == '__main__':
    db_name = environ.get('DB_NAME', 'db_graphql')
    db_user = environ.get('DB_USER', 'db_user')
    db_password = environ.get('DB_PASSWORD', 'db_password')
    engine = create_engine(
        f'postgresql+psycopg2://{db_user}:{db_password}@db/{db_name}'
    )

    with Session(engine) as session:
        email = sys.argv[1]
        password = sys.argv[2]
        print(email, password)

        if not email or not password:
            print('Введите почту и пароль')
        else:
            try:
                WorkersGateway.create_superuser(email, password, session)
            except ValueError as err:
                print(str(err))
