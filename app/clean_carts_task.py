from hotel_business.session.session import get_session
from hotel_business.gateways.carts_gateway import CartsGateway

if __name__ == '__main__':
    with get_session() as session:
        CartsGateway.clean_carts(session)
