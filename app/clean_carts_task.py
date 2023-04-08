from datetime import datetime, timedelta
from modules.settings import settings
from modules.models.orders import Cart
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session
from os import environ


if __name__ == '__main__':
    db_name = environ.get('DB_NAME', 'db_graphql')
    db_user = environ.get('DB_USER', 'db_user')
    db_password = environ.get('DB_PASSWORD', 'db_password')
    engine = create_engine(
        f'postgresql+psycopg2://{db_user}:{db_password}@db/{db_name}'
    )

    with Session(engine) as session:
        session.query(Cart).filter(
            Cart.date_created < datetime.now(tz=settings.TIMEZONE) - timedelta(hours=24)
        ).delete()
        session.commit()

