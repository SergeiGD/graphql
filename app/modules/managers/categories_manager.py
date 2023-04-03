from datetime import date, timedelta, datetime
from typing import Optional
from sqlalchemy import func, text, desc
from ..models.categories import Category
from ..models.rooms import Room
from ..models.tags import Tag, category_tag
from ..models.sales import Sale
from ..models.base import db
from ..models.orders import Purchase
from ..settings import settings


class CategoriesManager:
    """
    Класс для управления категориями
    """
    @staticmethod
    def pick_room(category: Category, start: date, end: date, purchase_id: Optional[int] = None):
        """
        Поиск свободной комнаты категории
        :param category: категория, у которой нужно найти комнату
        :param start: дата начала брони
        :param end: дата конца брони
        :param purchase_id: id покупки, если нужно подобрать комнату для обновления покупки, а не создания новой
        :return: id комнаты, если нашлась подходящая, иначе None
        """
        # комнат категории
        rooms = db.session.query(Room).filter(
            Room.date_deleted == None,
            Room.category_id == category.id,
        ).with_entities(Room.id).all()
        # id комнат категории
        free_rooms = {item[0] for item in rooms}
        # обявления первого дня проверки
        day_to_check = start

        while free_rooms and day_to_check < end:
            # занятые комнаты на проверяемую дату
            busy_rooms = db.session.query(Purchase).filter(
                Purchase.room_id.in_(free_rooms),
                Purchase.is_canceled == False,
                Purchase.start <= day_to_check,
                Purchase.end > day_to_check,
                Purchase.id != purchase_id
            ).with_entities(Purchase.room_id).all()

            # убираем занятые комнаты
            free_rooms -= {item[0] for item in busy_rooms}
            # передвигаем день
            day_to_check += timedelta(days=1)

        if not free_rooms:
            return None

        # т.к. может вернуться несколько подходящих комнат, возвращаем первую
        picked_room_id = list(free_rooms)[0]
        return picked_room_id

    @staticmethod
    def get_busy_dates(category: Category, date_start: date, date_end: date):
        """
        Получение занятых дней комнат категории
        :param category: категория, комнаты которой нужно проверить
        :param date_start: дата начала проверки
        :param date_end: дата конца проверки
        :return:
        """
        if date_end < date.today():
            # если запрашиваем прошедшие даты, то проверять смысла нету и возвращаем, что все занято
            return sorted([
                date_start + timedelta(days=x) for x in range((date_end - date_start).days + 1)
            ])

        current_day = date_start
        busy_dates = []
        while current_day <= date_end:
            # проверяем занят ли день и не прошедшая ли дата
            if current_day < date.today() or CategoriesManager.is_day_busy(category, current_day):
                busy_dates.append(current_day)
            current_day += timedelta(days=1)
        # сортируем даты
        busy_dates.sort()
        return busy_dates

    @staticmethod
    def is_day_busy(category: Category, day: date):
        """
        Проверка, забронированны ли все комнаты выбранной категории на этот день
        :param category: категория, комнаты которой нужно проверить
        :param day: дата, на которую будет осуществлена проверка
        :return:
        """
        # получаем брони, которые есть на этот день
        purchases = db.session.query(Purchase.room_id).filter(
            Purchase.start <= day,
            Purchase.end > day,
            Purchase.is_canceled == False
        ).subquery('purchases')

        # если есть хоть одна комната, на которую нету брони в этот день, то есть свободная
        if db.session.query(
                db.session.query(Room).filter(
                    Room.category_id == category.id,
                    Room.date_deleted == None,
                    Room.id.not_in(
                        purchases
                    )
                ).exists()
        ).scalar():
            return False
        return True

    @staticmethod
    def get_familiar(category: Category):
        """
        Получение похожих категория (с похожими тегами)
        :param category:  категория, для которой нужно найти похожие категории
        :return: список похожих категорий
        """

        # Получаем id тегов переданной категории
        tags = db.session.query(
            category_tag.c.tag_id
        ).filter(
            category_tag.c.tag_id.in_(
                db.session.query(category_tag.c.tag_id).filter(
                    category_tag.c.category_id == category.id
                )
            )
        )

        #  Получаем id категорий, у которых есть такие эе теги, как у переданной category
        cats = db.session.query(
            category_tag.c.category_id
        ).filter(
            category_tag.c.tag_id.in_(tags),
            category_tag.c.category_id != category.id
        )

        # получаем id 3-х категорий, у которых больше всего совпадений по тегам
        familiar_ids = db.session.query(
            category_tag.c.category_id.label('cat'),
            func.count(category_tag.c.tag_id).label('count'),
        ).filter(
            category_tag.c.category_id.in_(cats),
            category_tag.c.tag_id.in_(tags),
        ).group_by(text('cat'))\
            .order_by(desc('count'))\
            .limit(3)\
            .all()

        #  получаем сами объекты категорий из полученного кортежа (cat_id, count_tags)
        familiar_items = db.session.query(Category).filter(
            Category.id.in_([item[0] for item in familiar_ids])
        )
        return familiar_items

    @staticmethod
    def save_category(category: Category):
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def delete_category(category: Category):
        db.session.add(category)
        category.date_deleted = datetime.now(tz=settings.TIMEZONE)
        db.session.commit()

    @staticmethod
    def add_tag_to_category(category: Category, tag: Tag):
        db.session.add(category)
        category.tags.append(tag)
        db.session.commit()

    @staticmethod
    def remove_tag_from_category(category: Category, tag: Tag):
        db.session.add(category)
        category.tags.remove(tag)
        db.session.commit()

    @staticmethod
    def add_sale_to_category(category: Category, sale: Sale):
        db.session.add(category)
        category.sales.append(sale)
        db.session.commit()

    @staticmethod
    def remove_sale_to_category(category: Category, sale: Sale):
        db.session.add(category)
        category.sales.remove(sale)
        db.session.commit()
