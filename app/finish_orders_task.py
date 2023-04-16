from hotel_business_module.session.session import get_session
from hotel_business_module.gateways.orders_gateway import OrdersGateway

if __name__ == '__main__':
    with get_session() as session:
        OrdersGateway.finish_orders(session)
