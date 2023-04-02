from ..models.orders import Purchase, Order, Cart
from ..models.users import User, Client
from .clients_manager import ClientsManager
from .orders_manager import OrdersManager
from ..models.base import db


class CartsManger:
    @staticmethod
    def confirm_cart(cart: Cart, email: str, is_fully_paid: bool = False):
        client = db.session.query(User).filter(
            User.email == email,
        ).first()
        if client is None:
            client = Client(email=email)
            ClientsManager.save_client(client)
        order = Order(client=client)
        OrdersManager.save_order(order)
        db.session.query(Purchase).filter(
            Purchase.order_id == cart.id,
        ).update({'order_id': order.id})
        db.session.delete(cart)
        db.session.commit()
        if is_fully_paid:
            order.paid = cart.price
        else:
            order.paid = cart.prepayment
        OrdersManager.save_order(order)
        return order

    @staticmethod
    def save_cart(cart: Cart):
        db.session.add(cart)
        db.session.commit()

