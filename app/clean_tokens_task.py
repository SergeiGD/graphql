from datetime import datetime
from modules.settings import settings
from modules.models.tokens import Token
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
        session.query(Token).filter(
            or_(
                Token.is_used == True,
                Token.expires < datetime.now(tz=settings.TIMEZONE)
            )
        ).delete()
        session.commit()

