from datetime import datetime
from modules.settings import settings
from modules.models.orders import Order, Purchase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from os import environ


if __name__ == '__main__':
    db_name = environ.get('DB_NAME', 'db_graphql')
    db_user = environ.get('DB_USER', 'db_user')
    db_password = environ.get('DB_PASSWORD', 'db_password')
    engine = create_engine(
        f'postgresql+psycopg2://{db_user}:{db_password}@db/{db_name}',
    )

    with Session(engine) as session:
        session.query(Purchase).filter(
            Purchase.end < datetime.now(settings.TIMEZONE),
            Purchase.is_paid == False,
            Purchase.is_prepayment_paid == True,
        ).update({'is_canceled': True})

        session.query(Purchase).filter(
            Purchase.end < datetime.now(settings.TIMEZONE),
            Purchase.is_paid == False,
            Purchase.is_prepayment_paid == False,
        ).delete()

        session.query(Order).filter(
            Order.id.not_in(
                session.query(Purchase.order_id).filter(
                    Purchase.end > datetime.now(settings.TIMEZONE),
                )
            ),
            Order.price > 0
        ).update({'date_finished': datetime.now(tz=settings.TIMEZONE)})

        session.commit()

