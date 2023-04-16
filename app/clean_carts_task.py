from hotel_business_module.session.session import get_session
from hotel_business_module.gateways.carts_gateway import CartsGateway

if __name__ == '__main__':
    with get_session() as session:
        CartsGateway.clean_carts(session)
