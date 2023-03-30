from ariadne import QueryType, ObjectType, MutationType, ScalarType
from .scalars.date_scalar import serialize_date, parse_date_value
from .scalars.datetime_scalar import serialize_datetime, parse_datetime_value
from .resolvers.tags_resolvers import resolve_create_tag, resolve_update_tag, resolve_delete_tag, resolve_tags
from .resolvers.photos_resolvers import resolve_create_photo, resolve_update_photo, resolve_delete_photo, resolve_photos
from .resolvers.rooms_resolvers import resolve_create_room, resolve_update_room, resolve_delete_room, resolve_rooms
from .resolvers.sales_resolvers import resolve_create_sale, resolve_update_sale, resolve_delete_sale, resolve_sales
from .resolvers.clients_resolvers import resolve_create_client, resolve_update_client, resolve_clients
from .resolvers.orders_resolvers import resolve_create_order, resolve_update_order, resolve_cancel_order, resolve_orders
from .resolvers.purchases_resolvers import resolve_create_purchase, resolve_update_purchase, resolve_cancel_purchase, resolve_purchases
from .resolvers.categories_resolvers import (
    resolve_create_category, resolve_update_category, resolve_delete_category, resolve_categories,
    resolve_add_tag_to_category, resolve_remove_tag_from_category,
    resolve_add_sale_to_category, resolve_remove_sale_from_category,
    resolve_category_familiar, resolve_category_rooms
)

query = QueryType()
query.set_field('tags', resolve_tags)
query.set_field('photos', resolve_photos)
query.set_field('rooms', resolve_rooms)
query.set_field('sales', resolve_sales)
query.set_field('categories', resolve_categories)
query.set_field('clients', resolve_clients)
query.set_field('orders', resolve_orders)
query.set_field('purchases', resolve_purchases)

mutation = MutationType()
mutation.set_field('createTag', resolve_create_tag)
mutation.set_field('updateTag', resolve_update_tag)
mutation.set_field('deleteTag', resolve_delete_tag)
mutation.set_field('createPhoto', resolve_create_photo)
mutation.set_field('updatePhoto', resolve_update_photo)
mutation.set_field('deletePhoto', resolve_delete_photo)
mutation.set_field('createRoom', resolve_create_room)
mutation.set_field('updateRoom', resolve_update_room)
mutation.set_field('deleteRoom', resolve_delete_room)
mutation.set_field('createRoom', resolve_create_room)
mutation.set_field('updateRoom', resolve_update_room)
mutation.set_field('deleteRoom', resolve_delete_room)
mutation.set_field('createSale', resolve_create_sale)
mutation.set_field('updateSale', resolve_update_sale)
mutation.set_field('deleteSale', resolve_delete_sale)
mutation.set_field('createClient', resolve_create_client)
mutation.set_field('updateClient', resolve_update_client)
mutation.set_field('createOrder', resolve_create_order)
mutation.set_field('updateOrder', resolve_update_order)
mutation.set_field('cancelOrder', resolve_cancel_order)
mutation.set_field('createPurchase', resolve_create_purchase)
mutation.set_field('updatePurchase', resolve_update_purchase)
mutation.set_field('cancelPurchase', resolve_cancel_purchase)
mutation.set_field('addTagToCategory', resolve_add_tag_to_category)
mutation.set_field('removeTagFromCategory', resolve_remove_tag_from_category)
mutation.set_field('addSaleToCategory', resolve_add_sale_to_category)
mutation.set_field('removeSaleFromCategory', resolve_remove_sale_from_category)

category = ObjectType('Category')
category.set_field('familiar', resolve_category_familiar)
category.set_field('rooms', resolve_category_rooms)

datetime_scalar = ScalarType('Datetime')
datetime_scalar.set_serializer(serialize_datetime)
datetime_scalar.set_value_parser(parse_datetime_value)

date_scalar = ScalarType('Date')
date_scalar.set_serializer(serialize_date)
date_scalar.set_value_parser(parse_date_value)

