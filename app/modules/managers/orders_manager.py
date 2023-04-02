from _decimal import Decimal
from datetime import datetime

from sqlalchemy import or_
from ..models.orders import Purchase, Order
from ..models.base import db
from ..settings import settings


class OrdersManager:
    """
    Класс для управления заказами
    """
    @staticmethod
    def update_payment(order: Order):
        """
        Обновление статуса оплаты
        :param order: заказ, который необходимо обновить
        :return:
        """
        if isinstance(order.paid, float):
            # если обновляли и установили paid, то преводим к decimal
            paid = Decimal(order.paid)
            order.paid = round(paid, 2)

        if order.paid >= order.price and order.paid > 0:
            # если полностью оплачен
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_paid == False,
            ).update({'is_paid': True})
            if order.date_full_paid is None:
                order.date_full_paid = datetime.now(tz=settings.TIMEZONE)
            return

        if order.paid >= order.prepayment and order.paid > 0:
            # если оплачена предоплата
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_prepayment_paid == False,
            ).update({'is_prepayment_paid': True})
            if order.date_full_prepayment is None:
                order.date_full_prepayment = datetime.now(tz=settings.TIMEZONE)
            return

        if order.paid < order.prepayment:
            # если не оплачено вообще
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_prepayment_paid == True,
            ).update({'is_prepayment_paid': False, 'is_paid': False})
            order.date_full_prepayment = None
            order.date_full_paid = None
            return

        if order.paid < order.price:
            # если не оплачена предоплата
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_paid == True,
            ).update({'is_paid': False})
            order.date_full_paid = None
            return

    @staticmethod
    def save_order(order: Order):
        db.session.add(order)
        if order.id is not None:
            OrdersManager.update_payment(order)
        db.session.commit()

    @staticmethod
    def mark_as_canceled(order: Order):
        """
        Отметить заказ как отмененный
        :param order: заказ, который нужно отменить
        :return:
        """
        db.session.add(order)
        # устанавливаем дату отмены
        order.date_canceled = datetime.now(tz=settings.TIMEZONE)
        order.date_finished = None
        # отменяем оплаченные покупки
        db.session.query(Purchase).filter(
            Purchase.order_id == order.id,
            Purchase.is_canceled == False,
            or_(Purchase.is_paid == True, Purchase.is_prepayment_paid == True),
        ).update({'is_canceled': True})
        # удаляем не оплаченные покупки
        db.session.query(Purchase).filter(
            Purchase.order_id == order.id,
            Purchase.is_canceled == False,
            Purchase.is_paid == False,
            Purchase.is_prepayment_paid == False,
        ).delete()
        db.session.commit()

    @staticmethod
    def mark_as_paid(order: Order):
        order.paid = order.price
        OrdersManager.save_order(order)

