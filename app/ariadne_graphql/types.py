from ariadne import QueryType, ObjectType, MutationType, ScalarType, UnionType

from .resolvers.auth_resolvers import (
    resolve_login, resolve_sing_up, resolve_refresh, resolve_account_confirm,
    resolve_reset_confirm, resolve_request_reset
)
from .resolvers.carts_resolvers import resolve_create_cart, resolve_cart, resolve_confirm_cart
from .resolvers.categories_resolvers import (
    resolve_create_category, resolve_update_category, resolve_delete_category, resolve_categories,
    resolve_add_tag_to_category, resolve_remove_tag_from_category,
    resolve_add_sale_to_category, resolve_remove_sale_from_category,
    resolve_category_familiar, resolve_category_busy_dates
)
from .resolvers.client_orders_resolvers import (
    resolve_cancel_client_order, resolve_client_profile_orders, resolve_client_pay_order, resolve_profile_info
)
from .resolvers.clients_resolvers import (
    resolve_create_client, resolve_update_client, resolve_delete_client, resolve_clients, resolve_client_orders
)
from .resolvers.groups_resolvers import (
    resolve_create_group, resolve_update_group, resolve_delete_group, resolve_groups, resolve_group_permissions,
    resolve_add_permission_to_group, resolve_remove_permission_from_group, resolve_group_users
)
from .resolvers.orders_resolvers import (
    resolve_create_order, resolve_update_order, resolve_cancel_order, resolve_orders,
    resolve_order_client, resolve_order_purchases
)
from .resolvers.permissions_resolvers import resolve_permissions
from .resolvers.photos_resolvers import resolve_create_photo, resolve_update_photo, resolve_delete_photo, resolve_photos
from .resolvers.purchases_resolvers import (
    resolve_create_purchase, resolve_update_purchase, resolve_cancel_purchase,
    resolve_purchases, resolve_purchase_order,
    resolve_create_cart_purchase, resolve_update_cart_purchase, resolve_cancel_cart_purchase
)
from .resolvers.rooms_resolvers import (
    resolve_create_room, resolve_update_room, resolve_delete_room, resolve_rooms
)
from .resolvers.sales_resolvers import resolve_create_sale, resolve_update_sale, resolve_delete_sale, resolve_sales
from .resolvers.tags_resolvers import (
    resolve_create_tag, resolve_update_tag, resolve_delete_tag, resolve_tags,
)
from .resolvers.workers_resolvers import (
    resolve_create_worker, resolve_update_worker, resolve_delete_worker, resolve_workers,
    resolve_add_group_to_worker, resolve_remove_group_from_worker, resolve_worker_groups
)
from .scalars.date_scalar import serialize_date, parse_date_value
from .scalars.datetime_scalar import serialize_datetime, parse_datetime_value
from .unions.orders_union import resolve_order_type
from .unions.users_union import resolve_user_type

query = QueryType()
query.set_field('getTags', resolve_tags)
query.set_field('getPhotos', resolve_photos)
query.set_field('getRooms', resolve_rooms)
query.set_field('getSales', resolve_sales)
query.set_field('getCategories', resolve_categories)
query.set_field('getClients', resolve_clients)
query.set_field('getOrders', resolve_orders)
query.set_field('getPurchases', resolve_purchases)
query.set_field('getWorkers', resolve_workers)
query.set_field('getGroups', resolve_groups)
query.set_field('getPermissions', resolve_permissions)
query.set_field('getCart', resolve_cart)
query.set_field('getClientOrders', resolve_client_profile_orders)
query.set_field('getProfileInfo', resolve_profile_info)

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
mutation.set_field('createGroup', resolve_create_group)
mutation.set_field('updateGroup', resolve_update_group)
mutation.set_field('deleteGroup', resolve_delete_group)
mutation.set_field('createRoom', resolve_create_room)
mutation.set_field('updateRoom', resolve_update_room)
mutation.set_field('deleteRoom', resolve_delete_room)
mutation.set_field('createSale', resolve_create_sale)
mutation.set_field('updateSale', resolve_update_sale)
mutation.set_field('deleteSale', resolve_delete_sale)
mutation.set_field('createCategory', resolve_create_category)
mutation.set_field('updateCategory', resolve_update_category)
mutation.set_field('deleteCategory', resolve_delete_category)
mutation.set_field('createClient', resolve_create_client)
mutation.set_field('updateClient', resolve_update_client)
mutation.set_field('deleteClient', resolve_delete_client)
mutation.set_field('createWorker', resolve_create_worker)
mutation.set_field('updateWorker', resolve_update_worker)
mutation.set_field('deleteWorker', resolve_delete_worker)
mutation.set_field('createOrder', resolve_create_order)
mutation.set_field('updateOrder', resolve_update_order)
mutation.set_field('cancelOrder', resolve_cancel_order)
mutation.set_field('createCart', resolve_create_cart)
mutation.set_field('createPurchase', resolve_create_purchase)
mutation.set_field('updatePurchase', resolve_update_purchase)
mutation.set_field('cancelPurchase', resolve_cancel_purchase)
mutation.set_field('createCartPurchase', resolve_create_cart_purchase)
mutation.set_field('updateCartPurchase', resolve_update_cart_purchase)
mutation.set_field('cancelCartPurchase', resolve_cancel_cart_purchase)
mutation.set_field('confirmCart', resolve_confirm_cart)
mutation.set_field('cancelClientOrder', resolve_cancel_client_order)
mutation.set_field('payClientOrder', resolve_client_pay_order)
mutation.set_field('addTagToCategory', resolve_add_tag_to_category)
mutation.set_field('removeTagFromCategory', resolve_remove_tag_from_category)
mutation.set_field('addSaleToCategory', resolve_add_sale_to_category)
mutation.set_field('removeSaleFromCategory', resolve_remove_sale_from_category)
mutation.set_field('addGroupToWorker', resolve_add_group_to_worker)
mutation.set_field('removeGroupFromWorker', resolve_remove_group_from_worker)
mutation.set_field('addPermissionToGroup', resolve_add_permission_to_group)
mutation.set_field('removePermissionFromGroup', resolve_remove_permission_from_group)
mutation.set_field('login', resolve_login)
mutation.set_field('singUp', resolve_sing_up)
mutation.set_field('confirmAccount', resolve_account_confirm)
mutation.set_field('requestReset', resolve_request_reset)
mutation.set_field('confirmReset', resolve_reset_confirm)
mutation.set_field('refreshToken', resolve_refresh)

category = ObjectType('Category')
category.set_field('familiar', resolve_category_familiar)
category.set_field('bookedDates', resolve_category_busy_dates)

group = ObjectType('Group')
group.set_field('permissions', resolve_group_permissions)
group.set_field('users', resolve_group_users)

order = ObjectType('Order')
order.set_field('purchases', resolve_order_purchases)
order.set_field('client', resolve_order_client)

purchase = ObjectType('Purchase')
purchase.set_field('order', resolve_purchase_order)

worker = ObjectType('Worker')
worker.set_field('groups', resolve_worker_groups)

client = ObjectType('Client')
client.set_field('orders', resolve_client_orders)

datetime_scalar = ScalarType('Datetime')
datetime_scalar.set_serializer(serialize_datetime)
datetime_scalar.set_value_parser(parse_datetime_value)

date_scalar = ScalarType('Date')
date_scalar.set_serializer(serialize_date)
date_scalar.set_value_parser(parse_date_value)

user_union = UnionType('UserUnion', resolve_user_type)
base_order_union = UnionType('BaseOrderUnion', resolve_order_type)
