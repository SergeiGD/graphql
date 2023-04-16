from hotel_business.session.session import get_session
from hotel_business.gateways.orders_gateway import OrdersGateway

if __name__ == '__main__':
    with get_session() as session:
        OrdersGateway.finish_orders(session)
