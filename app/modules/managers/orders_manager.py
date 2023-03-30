from _decimal import Decimal
from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_
from ..models.orders import Purchase, Order
from ..models.categories import Category
from ..models.sales import Sale
from ..models.rooms import Room
from ..models.base import db
from .categories_manager import CategoriesManager
from ..settings import settings


class OrdersManager:
    @staticmethod
    def update_payment(order: Order):
        if isinstance(order.paid, float):
            paid = Decimal(order.paid)
            order.paid = round(paid, 2)
        if order.paid >= order.price and order.paid > 0:
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_paid == False,
            ).update({'is_paid': True})
            if order.date_full_paid is None:
                order.date_full_paid = datetime.now(tz=settings.TIMEZONE)
            return

        if order.paid >= order.prepayment and order.paid > 0:
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_prepayment_paid == False,
            ).update({'is_prepayment_paid': True})
            if order.date_full_prepayment is None:
                order.date_full_prepayment = datetime.now(tz=settings.TIMEZONE)
            return

        if order.paid < order.prepayment:
            db.session.query(Purchase).filter(
                Purchase.order_id == order.id,
                Purchase.is_canceled == False,
                Purchase.is_prepayment_paid == True,
            ).update({'is_prepayment_paid': False, 'is_paid': False})
            order.date_full_prepayment = None
            order.date_full_paid = None
            return

        if order.paid < order.price:
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
        db.session.add(order)
        order.date_canceled = datetime.now(tz=settings.TIMEZONE)
        order.date_finished = None
        db.session.query(Purchase).filter(
            Purchase.order_id == order.id,
            Purchase.is_canceled == False,
            or_(Purchase.is_paid == True, Purchase.is_prepayment_paid == True),
        ).update({'is_canceled': True})
        db.session.query(Purchase).filter(
            Purchase.order_id == order.id,
            Purchase.is_canceled == False,
            Purchase.is_paid == False,
            Purchase.is_prepayment_paid == False,
        ).delete()
        db.session.commit()


# class PurchasesManager:
#     @staticmethod
#     def set_price(purchase: Purchase):
#         category: Category = db.session.query(Room).get(purchase.room_id).category
#         delta_seconds: Decimal = (purchase.end - purchase.start).total_seconds()
#         SECONDS_IN_DAY: int = 86400
#         days: int = round(Decimal(delta_seconds / SECONDS_IN_DAY), 0)
#         default_price: Decimal = category.price * days
#         sale = db.session.query(func.max(Sale.discount)).filter(
#             Sale.start_date <= datetime.now(),
#             Sale.end_date >= datetime.now(),
#             Sale.date_deleted == None,
#             Sale.categories.any(id=category.id)
#         ).scalar()
#         if sale:
#             sale_ration = Decimal(sale / 100)
#             purchase.price = default_price - (default_price * sale_ration)
#         else:
#             purchase.price = default_price
#
#         prepayment_ratio = Decimal(category.prepayment_percent / 100)
#         purchase.prepayment = purchase.price * prepayment_ratio
#         refund_ratio = Decimal(category.refund_percent / 100)
#         purchase.refund = purchase.price * refund_ratio
#
#     @staticmethod
#     def set_room(purchase: Purchase, category: Category):
#         room_id = CategoriesManager.pick_room(
#             category=category,
#             start=purchase.start,
#             end=purchase.end,
#             purchase_id=purchase.id
#         )
#         if room_id is None:
#             raise ValueError('На эти даты нет свободных комнат этой категории')
#
#         purchase.room_id = room_id
#
#     @staticmethod
#     def save_purchase(purchase: Purchase, category: Optional[Category] = None):
#         db.session.add(purchase)
#         category = category if category is not None else purchase.room.category
#
#         PurchasesManager.set_room(purchase, category)
#         PurchasesManager.set_price(purchase)
#         db.session.commit()
#         OrdersManager.save_order(purchase.order)
#
#     @staticmethod
#     def mark_as_canceled(purchase: Purchase):
#         db.session.add(purchase)
#         if purchase.is_prepayment_paid or purchase.is_paid:
#             purchase.is_canceled = True
#         else:
#             db.session.delete(purchase)
#         db.session.commit()
